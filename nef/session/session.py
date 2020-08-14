import flask.sessions
import itsdangerous
import json
import config
import nef.database
import nef.utils
import run as context


class Session(dict, flask.sessions.SessionMixin):

    def __init__(self, initial=None, sid=None):
        self.sid = sid
        self.initial = initial
        super(Session, self).__init__(initial or ())

    def __setitem__(self, key, value):
        super(Session, self).__setitem__(key, value)

    def __getitem__(self, item):
        return super(Session, self).__getitem__(item)

    def __delitem__(self, key):
        super(Session, self).__delitem__(key)


class SessionInterfaceImpl(flask.sessions.SessionInterface):

    def __init__(self):
        self.session_class = Session
        self.db_session = nef.database.tb_session.TB_Session()

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self._generate_sid()
            return self.session_class(sid=sid)

        signer = self._get_signer(app)
        try:
            sid_as_bytes = signer.unsign(sid)
            sid = sid_as_bytes.decode()
        except itsdangerous.BadSignature:
            sid = self._generate_sid()
            return self.session_class(sid=sid)

        # db load
        result = self.db_session.fetch_one("select * from t_session where session_id = %s", (sid,))

        val = None
        if result is not None:
            val = result["value"]

        if val is not None:
            try:
                data = json.loads(val)
                return self.session_class(data, sid=sid)
            except:
                return self.session_class(sid=sid)

        return self.session_class(sid=sid)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expires = self.get_expiration_time(app, session)

        val = json.dumps(dict(session))

        # db save
        try:
            self.db_session.insert((session.sid, val, expires))
        except BaseException as e:
            context.app.logger.debug(e)
            try:
                self.db_session.execute("update t_session set `value`=%s, expire = %s where session_id=%s",
                                        (val, expires, session.sid))
            except BaseException as e2:
                context.app.logger.debug(e2)

        session_id = self._get_signer(app).sign(itsdangerous.want_bytes(session.sid))

        if expires == config.PERMANENT_SESSION_LIFETIME_TERMINATE_AFTER_CLOSE:
            response.set_cookie(app.session_cookie_name, session_id, httponly=httponly,
                                domain=domain, path=path, secure=secure)
        else:
            response.set_cookie(app.session_cookie_name, session_id,
                                max_age=expires.total_seconds(), httponly=httponly,
                                domain=domain, path=path, secure=secure)

    def get_expiration_time(self, app, session):
        """
        :return: datetime.timedelta
        """
        # if session.permanent:
        #     return app.permanent_session_lifetime
        # else:
        #     return datetime.timedelta(seconds=0)
        return app.permanent_session_lifetime

    @staticmethod
    def _generate_sid():
        return str(nef.utils.uuid.uuid_random())

    @staticmethod
    def _get_signer(_app):
        if not _app.secret_key:
            return None
        return itsdangerous.Signer(_app.secret_key, salt='flask-session', key_derivation='hmac')

"""
1. import xxx
2. from xxx import yyy

    第一种失败就采用第二种，原因未知
"""
import flask
import nef
from nef.session.session import SessionInterfaceImpl
from nef.bp import bp_audios, bp_videos
import datetime
import json


nef.config.init()

# remove default dir 'static'
app = flask.Flask(__name__, static_folder='', static_url_path='')
app.config["SESSION_COOKIE_NAME"] = nef.config.SESSION_COOKIE_NAME
app.config["SESSION_COOKIE_DOMAIN"] = nef.config.SESSION_COOKIE_DOMAIN
app.config["SESSION_COOKIE_PATH"] = nef.config.SESSION_COOKIE_PATH
app.config["SESSION_COOKIE_HTTPONLY"] = nef.config.SESSION_COOKIE_HTTPONLY
app.config["SESSION_COOKIE_SECURE"] = nef.config.SESSION_COOKIE_SECURE
app.config["SESSION_REFRESH_EACH_REQUEST"] = nef.config.SESSION_REFRESH_EACH_REQUEST
app.config["PERMANENT_SESSION_LIFETIME"] = nef.config.PERMANENT_SESSION_LIFETIME_TERMINATE_AFTER_CLOSE

# upload file
app.config['MAX_CONTENT_LENGTH'] = nef.config.UPLOAD_FILE_MAX_LENGTH

# static file
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = datetime.timedelta(seconds=5)

# session
"""

username + password登陆后从t_user中获取个人信息，
    而这些信息保存在浏览器端不安全，因此session产生了

1. session可以将这些信息保存在server端，在有效期内可以一直使用
2. session失效后，就需要重新登陆，然后重新把各种信息放在session中
3. server端提供接口获取session中的信息
例如：
@app.route("/info")
def info():
    result = {"name": flask.session.get("name", ""), "pwd": flask.session.get("pwd", "")}
    return result

"""
app.secret_key = nef.config.SECRET_KEY
app.session_interface = SessionInterfaceImpl()

# blueprint
app.register_blueprint(blueprint=bp_videos, url_prefix="/videos")
app.register_blueprint(blueprint=bp_audios, url_prefix="/audios")


@app.route("/")
@app.route("/index.html")
def index():
    return flask.render_template("welcome.html")


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("res/icon/globe.ico")


@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == "POST":
        username = None
        password = None

        content_type = ""
        for header in flask.request.headers:
            if "content-type" == header[0].lower():
                content_type = header[1]
        if nef.config.CONTENT_TYPE_APPLICATION_JSON in content_type.lower():
            username = json.loads(flask.request.data.decode("utf-8"))["username"]
            password = json.loads(flask.request.data.decode("utf-8"))["password"]
        else:
            if nef.config.CONTENT_TYPE_APPLICATION_URLENCODED in content_type.lower():
                username = flask.request.form.get("username", None)
                password = flask.request.form.get("password", None)
        try:
            db = nef.database.tb_user.TB_User()
            fetch_result = db.fetch_one("select * from t_user where username = %s", username)
            if fetch_result is None:
                return "User does not exist"
            if fetch_result["password"] != password:
                return "Password error"
            flask.session["user_id"] = fetch_result["user_id"]
        except BaseException as e:
            app.logger.debug(e)
            return str(e)
        return "success"
    return flask.render_template("login/login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        username = None
        email = None
        phone = None
        password = None

        content_type = ""
        for header in flask.request.headers:
            if "content-type" == header[0].lower():
                content_type = header[1]
        if nef.config.CONTENT_TYPE_APPLICATION_JSON in content_type.lower():
            # POST /info
            # Content-Type:application/json
            # '{"xxx": "xxx", "xxx": xx}'
            username = json.loads(flask.request.data.decode("utf-8"))["username"]
            email = json.loads(flask.request.data.decode("utf-8"))["email"]
            phone = json.loads(flask.request.data.decode("utf-8"))["phone"]
            password = json.loads(flask.request.data.decode("utf-8"))["password"]
        elif nef.config.CONTENT_TYPE_APPLICATION_URLENCODED in content_type.lower():
            # POST /info
            # Content-Type:application/x-www-form-urlencoded
            # "xxx=xx&&xxx=xx"
            username = flask.request.form.get("username", None)
            email = flask.request.form.get("email", None)
            phone = flask.request.form.get("phone", None)
            password = flask.request.form.get("password", None)

        try:
            db = nef.database.tb_user.TB_User()
            user_id = nef.utils.randoms.random_digital(length=15)
            db.insert(
                (user_id, username, username, password, 1, email, phone))
            flask.session["user_id"] = user_id
        except BaseException as e:
            app.logger.debug(e)
            return str(e)
        return flask.redirect(flask.url_for("login"))

    return flask.render_template("register/register.html")


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if flask.request.method == "POST":
        return "success"
    return flask.render_template("forgot_password/forgot_password.html")


@app.route("/logout")
def logout():
    flask.session.pop("user_id", None)
    return flask.redirect(flask.url_for("login"))


@app.errorhandler(400)
def error_handler_400(error):
    return str(error)


@app.errorhandler(404)
def error_handler_404(error):
    return str(error)


@app.before_request
def before_request():
    # app.logger.debug("before request")
    if flask.request.path != "/register" and flask.request.path != "/login" and flask.request.path != "/forgot_password":
        if flask.session.get("user_id", None) is None:
            app.logger.warning("not login")
        return None


@app.after_request
def after_request(request):
    # app.logger.debug("after request")
    return request


@app.teardown_request
def teardown_request(request):
    # app.logger.debug("teardown request")
    return request


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, ssl_context=("certificate/server.crt", "certificate/server.key"))

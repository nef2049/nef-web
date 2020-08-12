import flask
import bp
import config
import session.session
import database
import utils


config.init()

# remove default dir 'static'
app = flask.Flask(__name__, static_folder='', static_url_path='')
app.config["SESSION_COOKIE_NAME"] = config.SESSION_COOKIE_NAME
app.config["SESSION_COOKIE_DOMAIN"] = config.SESSION_COOKIE_DOMAIN
app.config["SESSION_COOKIE_PATH"] = config.SESSION_COOKIE_PATH
app.config["SESSION_COOKIE_HTTPONLY"] = config.SESSION_COOKIE_HTTPONLY
app.config["SESSION_COOKIE_SECURE"] = config.SESSION_COOKIE_SECURE
app.config["SESSION_REFRESH_EACH_REQUEST"] = config.SESSION_REFRESH_EACH_REQUEST
app.config["PERMANENT_SESSION_LIFETIME"] = config.PERMANENT_SESSION_LIFETIME_TERMINATE_AFTER_CLOSE

# upload file
app.config['MAX_CONTENT_LENGTH'] = config.UPLOAD_FILE_MAX_LENGTH

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
app.secret_key = config.SECRET_KEY
app.session_interface = session.session.SessionInterfaceImpl()

# blueprint
app.register_blueprint(blueprint=bp.bp_videos, url_prefix="/videos")
app.register_blueprint(blueprint=bp.bp_audios, url_prefix="/audios")


@app.route("/")
@app.route("/index.html")
def index():
    return flask.render_template("welcome.html")


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("res/icon/globe.ico")


@app.route("/login/<username>/<password>")
def login(username, password):
    flask.session["name"] = username
    flask.session["pwd"] = password
    try:
        db = database.tb_user.TB_User()
        db.insert((utils.randoms.random_digital(length=15), username, "steven", password, 1, "2942332923@qq.com",
                   "15313967539"))
    except BaseException as e:
        app.logger.debug(e)
    return "success"


@app.route("/test")
def test():
    flask.session["region"] = "shanghai"
    flask.session.pop("name", None)
    return "success"


@app.route("/info")
def info():
    result = {"name": flask.session.get("name", ""), "pwd": flask.session.get("pwd", "")}
    return result


@app.errorhandler(400)
def error_handler_400(error):
    return str(error)


@app.errorhandler(404)
def error_handler_404(error):
    return str(error)


# @app.before_request
# def before_request():
#     app.logger.debug("before request")
#
#
# @app.after_request
# def after_request(request):
#     app.logger.debug("after request")
#     return request
#
#
# @app.teardown_request
# def teardown_request(request):
#     app.logger.debug("teardown request")
#     return request


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, ssl_context=("certificate/server.crt", "certificate/server.key"))

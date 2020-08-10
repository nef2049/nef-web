import flask
import bp
import config


config.init()

# 去掉默认的static文件夹，
app = flask.Flask(__name__, static_folder='', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = config.UPLOAD_FILE_MAX_LENGTH

app.register_blueprint(blueprint=bp.bp_videos, url_prefix="/videos")
app.register_blueprint(blueprint=bp.bp_audios, url_prefix="/audios")


@app.route("/")
@app.route("/index.html")
def index():
    app.logger.debug(flask.url_for("static", filename="build/videos/black_widow.mp4"))
    return flask.render_template("welcome.html")


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("res/icon/globe.ico")


@app.errorhandler(404)
def error_handler_404(error):
    return str(error)


@app.before_request
def before_request():
    app.logger.debug("before request")


@app.after_request
def after_request(request):
    app.logger.debug("after request")
    return request


@app.teardown_request
def teardown_request(request):
    app.logger.debug("teardown request")
    return request


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

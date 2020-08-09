import flask
import bp

app = flask.Flask(__name__)

app.register_blueprint(blueprint=bp.bp_videos, url_prefix="/videos")
app.register_blueprint(blueprint=bp.bp_audios, url_prefix="/audios")

@app.route("/")
@app.route("/index.html")
def index():
    return "Hello Flask"

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("images/globe.ico")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

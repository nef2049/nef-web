from nef.bp import bp_blogs
from run import app


@bp_blogs.route("/")
def index():
    return app.send_static_file("index.html")

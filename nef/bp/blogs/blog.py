from nef.bp import bp_blogs
import flask


@bp_blogs.route("/")
def index():
    return flask.render_template("blog/index.html")

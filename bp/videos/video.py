import bp
import flask

@bp.bp_videos.route('/')
def hello_world():
    return 'Hello Videos'

@bp.bp_videos.route('/sample')
def sample():
    return flask.render_template("hello.html")

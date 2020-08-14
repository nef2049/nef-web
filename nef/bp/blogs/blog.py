from nef.bp import bp_blogs
from run import app


@bp_blogs.route("/<user_id>/")
def index(user_id):
    return app.send_static_file("user/" + user_id + "/index.html")

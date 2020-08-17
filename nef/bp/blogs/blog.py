from nef.bp import bp_blogs
from run import app
import flask
import werkzeug.utils
import run
import config
import os
import datetime
import nef.database
import json
import nef


ALLOWED_EXTENSIONS = {'md', 'markdown'}


@bp_blogs.route("/upload/<user_id>", methods=["POST"])
def upload(user_id):
    if not nef.does_user_exist(user_id):
        return {"code": 400, "status": "user not exists"}

    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)
    # /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads/428899288027429/posts
    file_path = os.path.join(config.UPLOAD_PATH, user_id + "/posts")

    if file and file_allowed(file_name):
        try:
            # database
            tb_posts = nef.database.tb_posts.TB_Posts()
            tb_posts.insert(
                (user_id,
                 file_name,
                 os.path.join(file_path, file_name),
                 datetime.datetime.now())
            )
            # save
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file.save(os.path.join(file_path, file_name))

            # configure user <user_id>
            config.config_user(user_id)

        except BaseException as e:
            run.app.logger.debug(e)
            return {"code": 400, "status": str(e)}
    else:
        return {"code": 400, "status": "type not allowed"}

    return {"code": 200, "status": "success"}


@bp_blogs.route("/delete/<user_id>", methods=["GET", "POST"])
def delete(user_id):
    if not nef.does_user_exist(user_id):
        return {"code": 400, "status": "user not exists"}

    if flask.request.method == "POST":
        content_type = ""
        for header in flask.request.headers:
            if "content-type" == header[0].lower():
                content_type = header[1]
        if "application/json" in content_type.lower():

            print(flask.request.data.decode("utf-8"))
            file_name = json.loads(flask.request.data.decode("utf-8"))["file_name"]
        else:
            file_name = flask.request.form.get("file_name", "")
    else:
        file_name = flask.request.args.get("file_name", "")

    if file_name == "":
        return {"code": 400, "status": "empty file name"}
    try:
        # database
        tb_posts = nef.database.tb_posts.TB_Posts()
        tb_posts.execute("delete from t_posts where user_id=%s and post_name=%s", (user_id, file_name))

        os.system('rm -f uploads/930214147537064/posts/{}'.format(file_name))

        config.config_user(user_id)
    except BaseException as e:
        return {"code": 400, "status": str(e)}
    return {"code": 200, "status": "success"}


@bp_blogs.route("/<user_id>/")
def index(user_id):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + user_id + "/index.html")


@bp_blogs.route("/<user_id>/tabs/categories/")
def tabs_categories(user_id):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + user_id + "/tabs/categories/index.html")


@bp_blogs.route("/<user_id>/tabs/tags/")
def tabs_tags(user_id):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + user_id + "/tabs/tags/index.html")


@bp_blogs.route("/<user_id>/tabs/archives/")
def tabs_archives(user_id):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + user_id + "/tabs/archives/index.html")


@bp_blogs.route("/<user_id>/tabs/about/")
def tabs_about(user_id):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + user_id + "/tabs/about/index.html")


@bp_blogs.route("/<user_id>/posts/<post_name>/")
def post(user_id, post_name):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + user_id + "/posts/" + post_name + "/index.html")


@bp_blogs.route("/<user_id>/tags/<tag>/")
def tags(user_id, tag):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + str(user_id) + "/tags/" + tag + "/index.html")


@bp_blogs.route("/<user_id>/categories/<category>/")
def categories(user_id, category):
    if not nef.does_user_login(user_id):
        return flask.redirect("/login")
    return app.send_static_file("user/" + str(user_id) + "/categories/" + category + "/index.html")


"""
# will also intercept the source files
# @bp_blogs.route("/<user_id>/<path:path>")
def accept_all(user_id, path):
    return app.send_static_file("user/" + str(user_id) + path + "/index.html")
"""


def file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

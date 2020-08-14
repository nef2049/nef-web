from nef.bp import bp_blogs
from run import app
import nef
import flask
import werkzeug.utils
import run
import config
import os
import datetime
import nef.database


ALLOWED_EXTENSIONS = {'md', 'markdown'}


@bp_blogs.route("/<user_id>/")
def index(user_id):
    return app.send_static_file("user/" + user_id + "/index.html")


@bp_blogs.route("/<user_id>/tabs/categories/")
def tabs_categories(user_id):
    return app.send_static_file("user/" + user_id + "/tabs/categories/index.html")


@bp_blogs.route("/<user_id>/tabs/tags/")
def tabs_tags(user_id):
    return app.send_static_file("user/" + user_id + "/tabs/tags/index.html")


@bp_blogs.route("/<user_id>/tabs/archives/")
def tabs_archives(user_id):
    return app.send_static_file("user/" + user_id + "/tabs/archives/index.html")


@bp_blogs.route("/<user_id>/tabs/about/")
def tabs_about(user_id):
    return app.send_static_file("user/" + user_id + "/tabs/about/index.html")


@bp_blogs.route("/<user_id>/posts/<post_name>/")
def post(user_id, post_name):
    return app.send_static_file("user/" + user_id + "/posts/" + post_name + "/index.html")


@bp_blogs.route("/upload/<user_id>", methods=["POST"])
def upload(user_id):
    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)
    # /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads/428899288027429/posts
    file_path = os.path.join(config.UPLOAD_PATH, user_id + "/posts")

    if file and allowed_file(file_name):
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
            # cp to jekyll then build then delete the post
            os.system('cp {0} {1}'.format(os.path.join(file_path, file_name),
                                          os.path.join(config.JEKYLL_POST_PATH, file_name)))

            user_path = os.path.join(config.JEKYLL_OUTPUT_PATH, str(user_id))
            cmd = '{0}/tools/build.sh -b {1} -d {2}'.format(
                config.JEKYLL_PROJECT_PATH,
                os.path.join("/user", str(user_id)),
                user_path
            )
            os.system(cmd)
            # delete file in jekyll
            os.system('rm {}'.format(os.path.join(config.JEKYLL_POST_PATH, file_name)))

        except BaseException as e:
            run.app.logger.debug(e)
            return {"code": 400, "status": str(e)}
    else:
        return {"code": 400, "status": "type not allowed"}

    return {"code": 200, "status": "success"}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

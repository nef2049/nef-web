from nef.bp import bp_images
import nef
import flask
import werkzeug.utils
import os
import config


ALLOWED_EXTENSIONS = {'jpg', 'png'}


@bp_images.route("/upload/<user_id>/avatar", methods=["POST"])
def upload_avatar(user_id):
    if not nef.does_user_exist(user_id):
        return {"code": 400, "status": "user not exists"}
    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)
    # /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads/428899288027429/avatar
    file_path = os.path.join(config.UPLOAD_PATH, user_id + "/avatar")

    if file and file_allowed(file_name):
        file_name_to_save = "avatar." + file_name.split('.')[1]
        file_path_to_save = os.path.join("/assets/img/avatar", file_name_to_save)
        print("file name " + file_path_to_save)

        # database
        tb_bc = nef.database.tb_blog_config.TB_Blog_Config()
        try:
            # database
            tb_bc.execute("insert into t_blog_config(user_id,avatar) values(%s,%s)", (user_id, file_path_to_save))
        except BaseException as e:
            try:
                tb_bc.execute("update t_blog_config set avatar=%s where user_id=%s", (user_id, file_path_to_save))
            except BaseException as e:
                return {"code": 400, "status": str(e)}

        # save
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file.save(os.path.join(file_path, file_name_to_save))

        # cp to static/user/xxx/assets/img/avatar/avatar.xxx
        if os.path.exists(config.JEKYLL_OUTPUT_PATH):
            avatar_path = config.JEKYLL_OUTPUT_PATH + "/" + str(user_id) + "/assets/img/avatar/"
            if not os.path.exists(avatar_path):
                os.makedirs(avatar_path)
            os.system('cp {0} {1}'.format(file_path + "/*", avatar_path))

    else:
        return {"code": 400, "status": "type not allowed"}

    return {"code": 200, "status": "success"}


def file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

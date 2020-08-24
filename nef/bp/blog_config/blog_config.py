from nef.bp import bp_blog_config
import nef.database
import flask
import config
import json
import werkzeug.utils
import os
import config


ALLOWED_EXTENSIONS = {"zip"}


@bp_blog_config.route("/<user_id>/update", methods=["POST"])
def update(user_id):
    """
    curl -X POST -d "title=Nef2049&&tagline=Now is everything&&author=nef&&github_username=reetmoon&&twitter_username=NEF2049&&social_name=nef&&social_email=steven199409@outlook.com&&social_links=https://twitter.com/NEF2049;https://weibo.com/5310322716/profile?rightmod=1&wvr=6&mod=personinfo&is_all=1&&url=http://119.45.209.174:2333" -H "Content-Type: application/x-www-form-urlencoded" http://119.45.209.174:2333/bc/987002467198862/update
    """
    title = None
    tagline = None
    url = None
    author = None
    avatar = None
    github_username = None
    twitter_username = None
    social_name = None
    social_email = None
    social_links = None

    content_type = ""
    for header in flask.request.headers:
        if "content-type" == header[0].lower():
            content_type = header[1]
    if config.CONTENT_TYPE_APPLICATION_JSON in content_type.lower():
        title = json.loads(flask.request.data.decode("utf-8"))["title"]
        tagline = json.loads(flask.request.data.decode("utf-8"))["tagline"]
        url = json.loads(flask.request.data.decode("utf-8"))["url"]
        author = json.loads(flask.request.data.decode("utf-8"))["author"]
        avatar = json.loads(flask.request.data.decode("utf-8"))["avatar"]
        github_username = json.loads(flask.request.data.decode("utf-8"))["github_username"]
        twitter_username = json.loads(flask.request.data.decode("utf-8"))["twitter_username"]
        social_name = json.loads(flask.request.data.decode("utf-8"))["social_name"]
        social_email = json.loads(flask.request.data.decode("utf-8"))["social_email"]
        social_links = json.loads(flask.request.data.decode("utf-8"))["social_links"]
    else:
        if config.CONTENT_TYPE_APPLICATION_URLENCODED in content_type.lower():
            title = flask.request.form.get("title", None)
            tagline = flask.request.form.get("tagline", None)
            url = flask.request.form.get("url", None)
            author = flask.request.form.get("author", None)
            avatar = flask.request.form.get("avatar", None)
            github_username = flask.request.form.get("github_username", None)
            twitter_username = flask.request.form.get("twitter_username", None)
            social_name = flask.request.form.get("social_name", None)
            social_email = flask.request.form.get("social_email", None)
            social_links = flask.request.form.get("social_links", None)

    tb_bc = nef.database.tb_blog_config.TB_Blog_Config()
    try:
        tb_bc.execute(
            "insert into t_blog_config(user_id,title,tagline,url,author,avatar,github_username,"
            "twitter_username,social_name,social_email,social_links) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ",
            (user_id, title, tagline, url, author, avatar, github_username, twitter_username,
             social_name,
             social_email, social_links)
        )
    except BaseException as e:
        try:
            tb_bc.execute(
                "update t_blog_config set title=%s,tagline=%s,url=%s,author=%s,avatar=%s,github_username=%s,"
                "twitter_username=%s,social_name=%s,social_email=%s,social_links=%s where user_id=%s",
                (title, tagline, url, author, avatar, github_username, twitter_username, social_name, social_email,
                 social_links, user_id))
        except BaseException as e:
            return str(e)

    config.config_user(user_id)
    return "success"


@bp_blog_config.route("/<user_id>/upload", methods=["POST"])
def upload(user_id):
    if not nef.does_user_exist(user_id):
        return {"code": 400, "status": "user not exists"}
    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)

    # /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads/428899288027429/favicons
    file_path = os.path.join(config.UPLOAD_PATH, str(user_id) + "/favicons")
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    if file and nef.utils.file.file_allowed(file_name, ALLOWED_EXTENSIONS):
        tb_bc = nef.database.tb_blog_config.TB_Blog_Config()
        try:
            tb_bc.execute("insert into t_blog_config(user_id,favicon_filename) values(%s,%s)", (user_id, file_name))
        except BaseException as e:
            print("insert error:" + str(e))
            try:
                tb_bc.execute("update t_blog_config set favicon_filename=%s where user_id=%s", (file_name, user_id))
            except BaseException as e:
                print("update error: " + str(e))
                return str(e)
        file.save(os.path.join(file_path, file_name))
        config.config_user(user_id)

    return "success"

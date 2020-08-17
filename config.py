import os
import datetime
import nef.database
import io
import yaml


# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision
PROJECT_PATH = os.path.split(os.path.abspath(__file__))[0]
# NefVision
PROJECT_NAME = os.path.split(PROJECT_PATH)[1]
# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads
UPLOAD_PATH = os.path.join(PROJECT_PATH, "uploads")

UPLOAD_PATH_AVATARS = os.path.join(UPLOAD_PATH, "avatars")
UPLOAD_PATH_AUDIOS = os.path.join(UPLOAD_PATH, "audios")
UPLOAD_PATH_VIDEOS = os.path.join(UPLOAD_PATH, "videos")

DB_ID_PREFIX = "nvid_"

# 2G bytes
UPLOAD_FILE_MAX_LENGTH = 8 * 1024 * 1024 * 1024

ULR_VIDEOS_PREFIX = "/uploads/videos"

SECRET_KEY = "4q356073da85fc469e9dc432046cb63d"

# session
SESSION_COOKIE_NAME = "nv-session"
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_PATH = None
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_REFRESH_EACH_REQUEST = True
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)
PERMANENT_SESSION_LIFETIME_TERMINATE_AFTER_CLOSE = datetime.timedelta(days=-1)

CONTENT_TYPE_APPLICATION_JSON = "application/json"
CONTENT_TYPE_APPLICATION_URLENCODED = "application/x-www-form-urlencoded"

# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/static/user
JEKYLL_OUTPUT_PATH = os.path.join(PROJECT_PATH, "static/user")
# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/jekyll-theme-chirpy
JEKYLL_PROJECT_PATH = os.path.join(PROJECT_PATH, "jekyll-theme-chirpy")
# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/jekyll-theme-chirpy/_posts
JEKYLL_POST_PATH = os.path.join(JEKYLL_PROJECT_PATH, "_posts")


def init():
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)

    if not os.path.exists(UPLOAD_PATH_AVATARS):
        os.makedirs(UPLOAD_PATH_AVATARS)

    if not os.path.exists(UPLOAD_PATH_AUDIOS):
        os.makedirs(UPLOAD_PATH_AUDIOS)

    if not os.path.exists(UPLOAD_PATH_VIDEOS):
        os.makedirs(UPLOAD_PATH_VIDEOS)

    if not os.path.exists(JEKYLL_PROJECT_PATH):
        clone_code = os.system('git clone https://github.com/cotes2020/jekyll-theme-chirpy.git')
        os.system('rm -f jekyll-theme-chirpy/_posts/*')

    if not os.path.exists(JEKYLL_OUTPUT_PATH):
        os.system('rm -rf static/user/*')
        os.makedirs(JEKYLL_OUTPUT_PATH)

        os.chdir(JEKYLL_PROJECT_PATH)
        bundle_install_code = os.system('bundle install')
        bash_init_code = os.system('tools/init.sh')
        os.chdir(PROJECT_PATH)


def config_user(user_id):
    # config _config.yml
    config_yaml_file(user_id)

    os.system('rm -rf static/user/{}/*'.format(user_id))
    # /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads/428899288027429/posts
    file_path = os.path.join(UPLOAD_PATH, str(user_id) + "/posts")

    if not os.path.exists(file_path):
        raise BaseException("path '" + file_path + "' not exists")

    try:
        db_posts = nef.database.tb_posts.TB_Posts()
        posts_result = db_posts.fetch_all("select * from t_posts where user_id=%s", user_id)
        for entry in posts_result:
            # cp xx/xx.md to jekyll then build then delete the post
            os.system('cp {0} {1}'.format(entry["post_path"],
                                          os.path.join(JEKYLL_POST_PATH, "")))
    except BaseException as e:
        import run
        run.app.logger.debug(str(e))

    user_path = os.path.join(JEKYLL_OUTPUT_PATH, str(user_id))
    cmd = '{0}/tools/build.sh -b {1} -d {2}'.format(
        JEKYLL_PROJECT_PATH,
        os.path.join("/user", str(user_id)),
        user_path
    )
    os.system(cmd)
    # delete file in jekyll
    os.system('rm {}'.format(os.path.join(JEKYLL_POST_PATH, "*")))


# file_path: /home/vaad/xxx/PythonProjects/NefVision/jekyll-theme-chirpy/_config.yml
def config_yaml_file(user_id):
    file_path = os.path.join(JEKYLL_PROJECT_PATH, "_config.yml")
    with io.open(file_path, 'r', encoding="utf-8") as rf:
        config_content = yaml.load(rf, Loader=yaml.FullLoader)

        try:
            db_user = nef.database.tb_user.TB_User()
            user_info = db_user.fetch_one("select * from t_user where user_id=%s", user_id)

            config_content["title"] = "nef2077"
            config_content["tagline"] = "NOW IS FLASK"
            config_content["url"] = "http://10.0.75.1:60000"
            config_content["author"] = user_info["username"]
            config_content["github"]["username"] = "reetmoon"
            config_content["twitter"]["username"] = "NEF2049"
            config_content["social"]["name"] = "nef2077"
            config_content["social"]["email"] = user_info["email"]
            config_content["social"]["links"][0] = "https://twitter.com/NEF2049"
            config_content["social"]["links"][1] = "https://github.com/reetmoon"
        except BaseException as e:
            import run
            run.app.logger.debug(str(e))

    with io.open(file_path, 'w', encoding="utf-8") as wf:
        yaml.dump(config_content, wf)

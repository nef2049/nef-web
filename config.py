import os
import datetime
import nef.database
import io
import yaml
from nef.constants import cmd_code
import platform


PLATFORM = platform.system()
PLATFORM_MACOS = "Darwin"
PLATFORM_WINDOWS = "Windows"
PLATFORM_LINUX = "Linux"

# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision
PROJECT_PATH = os.path.split(os.path.abspath(__file__))[0]
# NefVision
PROJECT_NAME = os.path.split(PROJECT_PATH)[1]
# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads
UPLOAD_PATH = os.path.join(PROJECT_PATH, "uploads")

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

    if not os.path.exists(UPLOAD_PATH_AUDIOS):
        os.makedirs(UPLOAD_PATH_AUDIOS)

    if not os.path.exists(UPLOAD_PATH_VIDEOS):
        os.makedirs(UPLOAD_PATH_VIDEOS)

    if not os.path.exists(JEKYLL_PROJECT_PATH):
        clone_code = os.system('git clone https://github.com/sleepy-zeo/jekyll-theme-chirpy')
        if clone_code != cmd_code.OS_CMD_CODE_SUCCESS:
            os.system('rm -rf jekyll-theme-chirpy')
            raise BaseException(
                "failed to execute 'git clone https://github.com/sleepy-zeo/jekyll-theme-chirpy, code: "
                + str(clone_code))
        os.system('rm -f jekyll-theme-chirpy/_posts/*')

    if not os.path.exists(JEKYLL_OUTPUT_PATH):
        os.system('rm -rf static/user/*')
        os.makedirs(JEKYLL_OUTPUT_PATH)

        os.chdir(JEKYLL_PROJECT_PATH)

        bundle_install_code = os.system('bundle install')
        if bundle_install_code != cmd_code.OS_CMD_CODE_SUCCESS:
            os.system('rm -rf static/user/')
            raise BaseException("failed to execute 'bundle install', code: " + str(bundle_install_code))

        bash_init_code = os.system('tools/init.sh')
        if bash_init_code != cmd_code.OS_CMD_CODE_SUCCESS:
            os.system('rm -rf static/user/')
            raise BaseException("failed to execute 'tools/init.sh', code: " + str(bash_init_code))

        os.chdir(PROJECT_PATH)


def config_user(user_id):
    print("111111111111111111111111111")

    # config _config.yml
    config_yaml_file(user_id)

    os.system('rm -rf static/user/{}/*'.format(user_id))
    # /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads/428899288027429/posts
    file_path = os.path.join(UPLOAD_PATH, str(user_id) + "/posts")

    if not os.path.exists(file_path):
        os.makedirs(file_path)

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

    try:
        db_bc = nef.database.tb_blog_config.TB_Blog_Config()
        posts_result = db_bc.fetch_one("select * from t_blog_config where user_id=%s", user_id)
        filename = posts_result["favicon_filename"]

        if filename is not None:
            os.system('rm -rf {}'.format(JEKYLL_PROJECT_PATH + "/assets/img/favicons/*"))
            os.system('cp {} {}'.format(
                os.path.join(os.path.join(UPLOAD_PATH, str(user_id) + "/favicons"), filename),
                JEKYLL_PROJECT_PATH + "/assets/img/favicons/"))
            os.chdir(JEKYLL_PROJECT_PATH + "/assets/img/favicons/")
            os.system("rm -rf *.png *.xml *.json")
            os.system("unzip {}".format(filename))
            os.system("rm {} {} {}".format(filename, "browserconfig.xml", "manifest.json"))
            os.chdir(PROJECT_PATH)

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

    # avatar
    # cp to static/user/xxx/assets/img/avatar/avatar.xxx
    if os.path.exists(JEKYLL_OUTPUT_PATH):
        avatar_path_src = os.path.join(UPLOAD_PATH, str(user_id) + "/avatar")
        avatar_path = JEKYLL_OUTPUT_PATH + "/" + str(user_id) + "/assets/img/avatar/"
        if not os.path.exists(avatar_path):
            os.makedirs(avatar_path)
        os.system('cp {0} {1}'.format(avatar_path_src + "/*", avatar_path))


# file_path: /home/vaad/xxx/PythonProjects/NefVision/jekyll-theme-chirpy/_config.yml
def config_yaml_file(user_id):
    file_path = os.path.join(JEKYLL_PROJECT_PATH, "_config.yml")
    with io.open(file_path, 'r', encoding="utf-8") as rf:
        config_content = yaml.load(rf, Loader=yaml.FullLoader)

        try:
            db_bc = nef.database.tb_blog_config.TB_Blog_Config()
            user_info = db_bc.fetch_one("select * from t_blog_config where user_id=%s", user_id)
            if user_info["title"] is not None:
                config_content["title"] = user_info["title"]
            if user_info["tagline"] is not None:
                config_content["tagline"] = user_info["tagline"]
            if user_info["url"] is not None:
                config_content["url"] = user_info["url"]
            if user_info["author"] is not None:
                config_content["author"] = user_info["author"]
            if user_info["avatar"] is not None:
                config_content["avatar"] = user_info["avatar"]
            if user_info["github_username"] is not None:
                config_content["github"]["username"] = user_info["github_username"]
            if user_info["twitter_username"] is not None:
                config_content["twitter"]["username"] = user_info["twitter_username"]
            if user_info["social_name"] is not None:
                config_content["social"]["name"] = user_info["social_name"]
            if user_info["social_email"] is not None:
                config_content["social"]["email"] = user_info["social_email"]
            if user_info["social_links"] is not None:
                links = user_info["social_links"].split(";")
                for i in range(len(links)):
                    config_content["social"]["links"][i] = links[i]

        except BaseException as e:
            import run
            run.app.logger.debug(str(e))

    with io.open(file_path, 'w', encoding="utf-8") as wf:
        yaml.dump(config_content, wf)

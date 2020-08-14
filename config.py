import os
import datetime
import nef.database


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

    # TODO: 删除/static
    # TODO: 遍历uploads/xxx，把每个user的posts拷贝到jekyll 然后build 然后删除(把下面的操作移动到这个遍历中进行)

    if not os.path.exists(JEKYLL_OUTPUT_PATH):
        os.system('rm -rf static/')
        os.system('git clone https://github.com/cotes2020/jekyll-theme-chirpy.git')

        os.makedirs(JEKYLL_OUTPUT_PATH)

        os.chdir(JEKYLL_PROJECT_PATH)
        os.system('bundle install')
        os.system('tools/init.sh')
        os.chdir(PROJECT_PATH)

    db = nef.database.tb_user.TB_User()
    fetch_result = db.fetch_all("select * from t_user")
    for entry in fetch_result:
        user_id = entry["user_id"]
        user_path = os.path.join(JEKYLL_OUTPUT_PATH, str(user_id))
        if not os.path.exists(user_path):
            cmd = '{0}/tools/build.sh -b {1} -d {2}'.format(
                JEKYLL_PROJECT_PATH,
                os.path.join("/user", str(user_id)),
                user_path
            )
            os.system(cmd)

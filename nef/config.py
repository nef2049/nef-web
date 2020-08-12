import os
import datetime


# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision
PROJECT_PATH = os.path.split(os.path.abspath(__file__))[0]
# NefVision
PROJECT_NAME = os.path.split(PROJECT_PATH)[1]
# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/uploads
UPLOAD_PATH = os.path.join(PROJECT_PATH, "uploads")

UPLOAD_PATH_AVATARS = os.path.join(UPLOAD_PATH, "avatars")
UPLOAD_PATH_AUDIOS = os.path.join(UPLOAD_PATH, "audios")
UPLOAD_PATH_VIDEOS = os.path.join(UPLOAD_PATH, "videos")

DB_ID_PREFIX = "nef_"

# 2G bytes
UPLOAD_FILE_MAX_LENGTH = 8 * 1024 * 1024 * 1024

RELATIVE_PATH_HTML_TO_VIDEOS = "../uploads/videos"
ULR_VIDEOS_PREFIX = "http://10.0.75.1:8080/uploads/videos"

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


def init():
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)

    if not os.path.exists(UPLOAD_PATH_AVATARS):
        os.makedirs(UPLOAD_PATH_AVATARS)

    if not os.path.exists(UPLOAD_PATH_AUDIOS):
        os.makedirs(UPLOAD_PATH_AUDIOS)

    if not os.path.exists(UPLOAD_PATH_VIDEOS):
        os.makedirs(UPLOAD_PATH_VIDEOS)

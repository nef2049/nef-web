import os


# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision
PROJECT_PATH = os.path.split(os.path.abspath(__file__))[0]
# NefVision
PROJECT_NAME = os.path.split(PROJECT_PATH)[1]
# /home/vaad/snapdragon-high-med-2020-spf-2-0_amss_standard_oem/PythonProjects/NefVision/build
UPLOAD_PATH = os.path.join(PROJECT_PATH, "build")

UPLOAD_PATH_AUDIOS = os.path.join(UPLOAD_PATH, "audios")
UPLOAD_PATH_VIDEOS = os.path.join(UPLOAD_PATH, "videos")

DB_ID_PREFIX = "nef_"

# 2G bytes
UPLOAD_FILE_MAX_LENGTH = 8 * 1024 * 1024 * 1024

URL_VIDEO_PREFIX = "http://192.168.123.225/build/videos"


def init():
    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)

    if not os.path.exists(UPLOAD_PATH_AUDIOS):
        os.makedirs(UPLOAD_PATH_AUDIOS)

    if not os.path.exists(UPLOAD_PATH_VIDEOS):
        os.makedirs(UPLOAD_PATH_VIDEOS)

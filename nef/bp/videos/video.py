from nef.bp import bp_videos
import nef.database
import nef.utils
import config
import flask
import werkzeug.utils
import os
import run


@bp_videos.route('/')
def hello_world():
    return 'Hello Videos'


@bp_videos.route("/list")
def list():
    tb_videos = nef.database.tb_videos.TB_Videos()
    result = tb_videos.fetch_all("select * from t_videos")
    return str(result)


@bp_videos.route('/sample/<video_name>')
def sample(video_name):
    flask.session["video_name"] = video_name
    return flask.render_template("videos_sample.html")


@bp_videos.route("/selected")
def selected():
    db = nef.database.tb_videos.TB_Videos()
    result = db.fetch_one("select * from t_videos where name = %s", flask.session.get("video_name", ""))
    selected_video_name = ""
    if result is not None:
        selected_video_name = result["name"] + "." + result["file_type"]
    return os.path.join(config.ULR_VIDEOS_PREFIX, selected_video_name)


@bp_videos.route("/upload", methods=["POST"])
def upload():
    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)

    _file_name = nef.utils.file.get_file_name(file_name)
    _file_type = nef.utils.file.get_file_type(file_name)
    run.app.logger.debug(file_name)

    try:
        # save to database
        tb_videos = nef.database.tb_videos.TB_Videos()
        tb_videos.insert((config.DB_ID_PREFIX + nef.utils.uuid.uuid_random(),
                          _file_name,
                          _file_name,
                          os.path.join(config.UPLOAD_PATH_VIDEOS, file_name),
                          _file_type))
        file.save(os.path.join(config.UPLOAD_PATH_VIDEOS, file_name))
    except BaseException as e:
        run.app.logger.debug(e)
        return {"code": 400, "status": str(e)}

    return {"code": 200, "status": "success"}


@bp_videos.route("/download", methods=["GET"])
def download():
    return flask.send_from_directory("build/videos", "black_mirror.mp4", as_attachment=True)

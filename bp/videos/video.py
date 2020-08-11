import bp
import flask
import werkzeug.utils
import config
import os
import database
import utils
import app


selected_video_name = ""


@bp.bp_videos.route('/')
def hello_world():
    return 'Hello Videos'


@bp.bp_videos.route("/list")
def list():
    tb_videos = database.tb_videos.TB_Videos()
    result = tb_videos.fetch_all("select * from t_videos")
    return str(result)


@bp.bp_videos.route('/sample/<video_name>')
def sample(video_name):
    global selected_video_name
    selected_video_name = video_name
    return flask.render_template("videos_sample.html")


@bp.bp_videos.route("/selected")
def selected():
    return os.path.join(config.ULR_VIDEOS_PREFIX, selected_video_name)


@bp.bp_videos.route("/upload", methods=["POST"])
def upload():
    file = flask.request.files["file"]
    file_name = werkzeug.utils.secure_filename(file.filename)

    _file_name = utils.file.get_file_name(file_name)
    _file_type = utils.file.get_file_type(file_name)
    app.app.logger.debug(file_name)

    try:
        # save to database
        tb_videos = database.tb_videos.TB_Videos()
        tb_videos.insert((config.DB_ID_PREFIX + utils.uuid.uuid_ramdom(),
                          _file_name,
                          _file_name,
                          os.path.join(config.UPLOAD_PATH_VIDEOS, file_name),
                          _file_type))
        file.save(os.path.join(config.UPLOAD_PATH_VIDEOS, file_name))
    except BaseException as e:
        app.app.logger.debug(e)
        return {"code": 400, "status": str(e)}

    return {"code": 200, "status": "success"}


@bp.bp_videos.route("/download", methods=["GET"])
def download():
    return flask.send_from_directory("build/videos", "black_mirror.mp4", as_attachment=True)

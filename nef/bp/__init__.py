import flask


bp_blogs = flask.Blueprint("bp_blogs", __name__)
bp_videos = flask.Blueprint("bp_videos", __name__)
bp_audios = flask.Blueprint("bp_audios", __name__)

import nef.bp.blogs
import nef.bp.audios
import nef.bp.videos

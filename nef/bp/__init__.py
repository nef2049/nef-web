import flask


bp_blogs = flask.Blueprint("bp_blogs", __name__)
bp_videos = flask.Blueprint("bp_videos", __name__)
bp_audios = flask.Blueprint("bp_audios", __name__)
bp_images = flask.Blueprint("bp_images", __name__)
bp_blog_config = flask.Blueprint("bp_blog_config", __name__)

import nef.bp.blogs
import nef.bp.audios
import nef.bp.videos
import nef.bp.images
import nef.bp.blog_config

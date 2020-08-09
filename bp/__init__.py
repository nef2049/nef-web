"""
__init__.py的作用就是import所有的模块和子包，
    子包中的模块和子包由子包中的__init__.py来import
"""

import flask

bp_videos = flask.Blueprint("bp_videos", __name__)
bp_audios = flask.Blueprint("bp_audios", __name__)

import bp.videos
import bp.audios

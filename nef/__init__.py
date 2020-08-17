"""
 1. 导入模块
 2. 导入子包
"""

import nef.bp
import nef.database
import nef.session
import nef.utils

import flask


def does_user_exist(user_id):
    db_user = nef.database.tb_user.TB_User()
    return db_user.fetch_one("select * from t_user where user_id=" + str(user_id)) is not None


def does_user_login(user_id):
    return flask.session is not None and str(flask.session.get("user_id", "")) == str(user_id)

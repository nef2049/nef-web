import database


class TB_Session(object):

    def __init__(self):
        TB_Session.__create_database_if_not_exists()
        self.create_table_if_not_exists()

    @staticmethod
    def __create_database_if_not_exists():
        db = database.SQLManager()
        db.execute("create database if not exists NefVision")

    def create_table_if_not_exists(self):
        with database.SQLManager("NefVision") as db:
            db.execute("create table if not exists t_session("
                       "session_id varchar(128) not null,"
                       "`value` varchar(4096) not null,"
                       "expire time default null,"
                       "update_time timestamp default current_timestamp,"
                       "primary key(session_id))")

    def insert(self, args=None):
        with database.SQLManager("NefVision") as db:
            db.execute("insert into t_session(session_id,`value`,expire) values(%s,%s,%s)", args)

    def execute(self, sql, args=None):
        with database.SQLManager("NefVision") as db:
            db.execute(sql, args)

    def fetch_one(self, sql, args=None):
        with database.SQLManager("NefVision") as db:
            return db.fetch_one(sql, args)

    def fetch_all(self, sql, args=None):
        with database.SQLManager("NefVision") as db:
            return db.fetch_all(sql, args)

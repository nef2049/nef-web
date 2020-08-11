import database


class TB_Session(object):

    def __init__(self):
        TB_Session.create_database_if_not_exists()
        self.create_table_if_not_exists()

    @staticmethod
    def create_database_if_not_exists():
        db = database.SQLManager()
        db.execute("create database if not exists NefVision")

    @staticmethod
    def create_table_if_not_exists():
        with database.SQLManager("NefVision") as db:
            db.execute("create table if not exists t_session("
                       "session_id varchar(64) not null,"
                       "`value` varchar(512) not null,"
                       "expire time default null,"
                       "update_time timestamp default current_timestamp,"
                       "primary key(session_id))")

    @staticmethod
    def insert(args=None):
        with database.SQLManager("NefVision") as db:
            db.execute("insert into t_session(session_id,`value`,expire) values(%s,%s,%s)", args)

    @staticmethod
    def execute(sql, args=None):
        with database.SQLManager("NefVision") as db:
            db.execute(sql, args)

    @staticmethod
    def fetch_one(sql, args=None):
        with database.SQLManager("NefVision") as db:
            return db.fetch_one(sql, args)

    @staticmethod
    def fetch_all(sql, args=None):
        with database.SQLManager("NefVision") as db:
            return db.fetch_all(sql, args)

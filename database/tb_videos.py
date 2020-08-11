import database


class TB_Videos(object):

    def __init__(self):
        TB_Videos.__create_database_if_not_exists()
        self.create_table_if_not_exists()

    @staticmethod
    def __create_database_if_not_exists():
        db = database.SQLManager()
        db.execute("create database if not exists NefVision")

    def create_table_if_not_exists(self):
        with database.SQLManager("NefVision") as db:
            db.execute("create table if not exists t_videos("
                       "id varchar(128) not null,"
                       "`name` varchar(512) not null,"
                       "alias varchar(512),"
                       "path varchar(4096) not null,"
                       "file_type varchar(64) not null,"
                       "upload_time timestamp default current_timestamp ,"
                       "primary key(id),"
                       "unique uk_name(`name`))")

    def insert(self, args=None):
        with database.SQLManager("NefVision") as db:
            db.execute("insert into t_videos(id,`name`,alias,path,file_type) values(%s,%s,%s,%s,%s)", args)

    def fetch_one(self, sql, args=None):
        with database.SQLManager("NefVision") as db:
            return db.fetch_one(sql, args)

    def fetch_all(self, sql, args=None):
        with database.SQLManager("NefVision") as db:
            return db.fetch_all(sql, args)

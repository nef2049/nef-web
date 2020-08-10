import database


class TB_Videos(object):

    def __init__(self):
        TB_Videos.create_database_if_not_exists()
        self.db = database.SQLManager("NefVision")
        self.create_table_if_not_exists()

    @staticmethod
    def create_database_if_not_exists():
        db = database.SQLManager()
        db.execute("create database if not exists NefVision")

    def create_table_if_not_exists(self):
        self.db.execute("create table if not exists t_videos("
                        "id varchar(64) not null,"
                        "`name` varchar(128) not null,"
                        "alias varchar(128),"
                        "path varchar(128) not null,"
                        "file_type varchar(32) not null,"
                        "upload_time timestamp default current_timestamp ,"
                        "primary key(id),"
                        "unique uk_name(`name`))")

    def insert(self, args=None):
        self.db.execute("insert into t_videos(id,`name`,alias,path,file_type) values(%s,%s,%s,%s,%s)", args)

    def print(self):
        return self.db.get_one("select * from t_videos")

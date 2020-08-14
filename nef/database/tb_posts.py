import nef.database


class TB_Posts(object):

    def __init__(self):
        TB_Posts.__create_database_if_not_exists()
        self.create_table_if_not_exists()

    @staticmethod
    def __create_database_if_not_exists():
        db = nef.database.SQLManager()
        db.execute("create database if not exists NefVision")

    def create_table_if_not_exists(self):
        with nef.database.SQLManager("NefVision") as db:
            db.execute("create table if not exists t_posts("
                       "id int not null auto_increment,"
                       "user_id bigint(15) not null,"
                       "post_name varchar(64) not null,"
                       "post_path varchar(4096) not null,"
                       "create_time timestamp default current_timestamp,"
                       "upload_time timestamp default current_timestamp on update current_timestamp,"
                       "primary key(id),"
                       "constraint fk_user_id foreign key(user_id) references t_user(user_id) on update cascade)")

    def insert(self, args=None):
        with nef.database.SQLManager("NefVision") as db:
            db.execute("insert into t_posts(user_id,post_name,post_path,create_time) values(%s,%s,%s,%s)", args)

    def execute(self, sql, args=None):
        with nef.database.SQLManager("NefVision") as db:
            db.execute(sql, args)

    def fetch_one(self, sql, args=None):
        with nef.database.SQLManager("NefVision") as db:
            return db.fetch_one(sql, args)

    def fetch_all(self, sql, args=None):
        with nef.database.SQLManager("NefVision") as db:
            return db.fetch_all(sql, args)

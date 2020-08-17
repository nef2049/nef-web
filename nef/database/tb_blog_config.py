import nef.database


class TB_Blog_Config(object):

    def __init__(self):
        TB_Blog_Config.__create_database_if_not_exists()
        self.create_table_if_not_exists()

    @staticmethod
    def __create_database_if_not_exists():
        db = nef.database.SQLManager()
        db.execute("create database if not exists NefVision")

    def create_table_if_not_exists(self):
        with nef.database.SQLManager("NefVision") as db:
            db.execute("create table if not exists t_blog_config("
                       "id bigint(15) not null auto_increment,"
                       "user_id bigint(15) not null,"
                       "title varchar(64) default null,"
                       "tagline varchar(256) default null,"
                       "url varchar(64) default null,"
                       "author varchar(64) default null,"
                       "avatar varchar(128) default '/assets/img/sample/avatar.jpg',"
                       "github_username varchar(64) default null,"
                       "twitter_username varchar(64) default null,"
                       "social_name varchar(64) default null,"
                       "social_email varchar(64) default null,"
                       "social_links varchar(512) default null,"
                       "register_time timestamp default current_timestamp,"
                       "update_time timestamp default current_timestamp on update current_timestamp,"
                       "primary key(id),"
                       "unique uk_bc_user_id(user_id),"
                       "constraint fk_bc_user_id foreign key(user_id) references t_user(user_id) on update cascade)")

    def insert(self, args=None):
        with nef.database.SQLManager("NefVision") as db:
            db.execute(
                "insert into t_blog_config(user_id) "
                "values(%s)", args)

    def execute(self, sql, args=None):
        with nef.database.SQLManager("NefVision") as db:
            db.execute(sql, args)

    def fetch_one(self, sql, args=None):
        with nef.database.SQLManager("NefVision") as db:
            return db.fetch_one(sql, args)

    def fetch_all(self, sql, args=None):
        with nef.database.SQLManager("NefVision") as db:
            return db.fetch_all(sql, args)

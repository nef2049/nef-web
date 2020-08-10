import pymysql


DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "passwd": "1994",
    "charset": "utf8"
}


class SQLManager(object):

    # 初始化实例方法
    def __init__(self, db_name=None):
        self.conn = None
        self.cursor = None
        self.db_name = db_name
        self.__connect()

    # 进入with语句自动执行
    def __enter__(self):
        return self

    # 退出with语句块自动执行
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()

    # 连接数据库
    def __connect(self):
        if self.db_name is None:
            self.conn = pymysql.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                port=DB_CONFIG["port"],
                passwd=DB_CONFIG["passwd"],
                charset=DB_CONFIG["charset"]
            )
        else:
            self.conn = pymysql.connect(
                host=DB_CONFIG["host"],
                user=DB_CONFIG["user"],
                port=DB_CONFIG["port"],
                passwd=DB_CONFIG["passwd"],
                db=self.db_name,
                charset=DB_CONFIG["charset"]
            )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭数据库cursor和连接
    def __close(self):
        self.cursor.close()
        self.conn.close()

    # 查询多条数据
    def get_list(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    # 查询单条数据
    def get_one(self, sql, args=None):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    # 执行单条SQL语句
    def execute(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()

    # 创建单条记录的语句
    def execute_id(self, sql, args=None):
        self.cursor.execute(sql, args)
        self.conn.commit()
        last_id = self.cursor.lastrowid
        return last_id

    # 执行多条SQL语句
    def multi_execute(self, sql, args=None):
        """

        :param sql: insert into table(id,name) values(%s,%s)
        :param args: [(1,'小明'),(2,'zeke'),(3,'琦琦'),(4,'韩梅梅')]
        :return:
        """
        self.cursor.executemany(sql, args)
        self.conn.commit()


import database.tb_videos

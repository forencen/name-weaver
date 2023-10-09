import sqlite3


class SQLiteDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        创建表格
        :param table_name: 表格名称
        :param columns: 列定义，例如：'id INTEGER PRIMARY KEY, name TEXT, age INTEGER'
        """
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def insert_data(self, table_name, data):
        """
        插入数据
        :param table_name: 表格名称
        :param data: 插入的数据，字典形式
        """
        placeholders = ', '.join(['?'] * len(data))
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        insert_sql = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(insert_sql, values)
        self.conn.commit()

    def insert_multiple_data(self, table_name, data_list):
        """
        批量插入数据
        :param table_name: 表格名称
        :param data_list: 插入的数据列表，每个元素是一个字典
        """
        for data in data_list:
            placeholders = ', '.join(['?'] * len(data))
            columns = ', '.join(data.keys())
            values = tuple(data.values())
            insert_sql = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.cursor.execute(insert_sql, values)

        self.conn.commit()

    def query_data(self, sql):
        """
        查询数据
        :return: 查询结果，列表形式
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        """
        关闭数据库连接
        """
        self.conn.close()


# 使用示例
if __name__ == "__main__":
    # 创建一个SQLite数据库实例
    db = SQLiteDB('kangxi.db')

    # 创建表格
    db.create_table('word', 'id INTEGER PRIMARY KEY, name TEXT, age INTEGER')

    # 插入数据
    user_data = {'name': 'Alice', 'age': 25}
    db.insert_data('users', user_data)

    # 查询数据
    result = db.query_data('users', '*', 'age > 20')
    print(result)

    # 关闭数据库连接
    db.close()

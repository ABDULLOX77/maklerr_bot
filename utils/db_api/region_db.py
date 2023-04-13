import sqlite3


class DatabaseRegion:
    def __init__(self, path_to_db="region.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        with sqlite3.connect(self.path_to_db) as connection:
            connection.set_trace_callback(logger)
            cursor = connection.cursor()
            data = None
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            if fetchall:
                data = cursor.fetchall()
            if fetchone:
                data = cursor.fetchone()
        return data

    def create_table_region(self):
        sql = """
        CREATE TABLE Region (
            status varchar(20),
            region varchar(20),
            farqiyo varchar(20)
        );
        """
        self.execute(sql, commit=True)

    def add_data(self, status: str, region: str, farqiyo: str):
        sql = """
            INSERT INTO Region (status, region, farqiyo) VALUES (?, ?, ?)
            """
        self.execute(sql, parameters=(status, region, farqiyo), commit=True)

    def select_region(self, farqiyo: str):
        sql = f"SELECT * FROM Region WHERE farqiyo = '{farqiyo}'"
        return self.execute(sql, fetchall=True)

    def update_region(self, farqiyo: str, region: str):
        sql = """
        UPDATE Region SET region = ? WHERE farqiyo = ?;
        """
        self.execute(sql, (region, farqiyo), commit=True)

    def update_status(self, farqiyo: str, status: str):
        sql = """
        UPDATE Region SET status = ? WHERE farqiyo = ?;
        """
        self.execute(sql, (status, farqiyo), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")

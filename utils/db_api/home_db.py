import sqlite3


class DatabaseHome:
    def __init__(self, path_to_db="homes.db"):
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

    def create_table_homes(self):
        sql = """
        CREATE TABLE Homes (
            id INTEGER NOT NULL UNIQUE,
            status varchar(20),
            region varchar(20) NOT NULL,
            rooms integer NOT NULL,
            photos varchar(50),
            home_data varchar(1000) NOT NULL,
            price integer NOT NULL,
            phone_number varchar(20) NOT NULL,
            PRIMARY KEY(id AUTOINCREMENT)
            );
        """
        self.execute(sql, commit=True)

    @staticmethod
    def formatArgs(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_data(self, status: str, region: str, rooms: int,  photos: str, home_data: str, price: int, phone_number: str):
        sql = """
            INSERT INTO Homes (status, region, rooms, photos, home_data, price, phone_number) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        self.execute(sql, parameters=(status, region, rooms, photos, home_data, price, phone_number), commit=True)

    def select_all_homes(self):
        sql = """
        SELECT * FROM Homes
        """
        return self.execute(sql, fetchall=True)

    def select_region(self, region):
        sql = f"SELECT * FROM Homes WHERE region = '{region}'"
        return self.execute(sql, fetchall=True)

    def select_status(self, status):
        sql = f"SELECT * FROM Homes WHERE status = '{status}'"
        return self.execute(sql, fetchall=True)

    def select_rooms(self, rooms):
        sql = f"SELECT * FROM Homes WHERE rooms = '{rooms}'"
        return self.execute(sql, fetchall=True)

    def select_id(self, home_id):
        sql = f"SELECT * FROM Homes WHERE id = '{home_id}'"
        return self.execute(sql, fetchall=True)


    def delete_home(self, home_id: int):
        self.execute(f"DELETE FROM Homes WHERE id = '{home_id}'", commit=True)

    def update_region(self, home_id, region):
        sql = """
        UPDATE Homes SET region = ? WHERE id = ?;
        """
        self.execute(sql, (region, home_id), commit=True)

    def update_rooms(self, home_id, rooms):
        sql = """
        UPDATE Homes SET rooms = ? WHERE id = ?;
        """
        self.execute(sql, (rooms, home_id), commit=True)

    def update_photos(self, home_id, photos):
        sql = """
        UPDATE Homes SET photos = ? WHERE id = ?;
        """
        self.execute(sql, (photos, home_id), commit=True)

    def update_home_data(self, home_id, home_data):
        sql = """
        UPDATE Homes SET home_data = ? WHERE id = ?;
        """
        self.execute(sql, (home_data, home_id), commit=True)

    def update_price(self, home_id, price):
        sql = """
        UPDATE Homes SET price = ? WHERE id = ?;
        """
        self.execute(sql, (price, home_id), commit=True)

    def update_phone_number(self, home_id, phone_number):
        sql = """
        UPDATE Homes SET phone_number = ? WHERE id = ?;
        """
        self.execute(sql, (phone_number, home_id), commit=True)

    def count_homes(self):
        return self.execute(f"SELECT COUNT(*) FROM Homes", fetchone=True)

    def get_last_data(self):
        return self.execute("SELECT MAX(id), * FROM Homes", fetchall=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")

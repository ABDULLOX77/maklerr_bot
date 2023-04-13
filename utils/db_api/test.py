from utils.db_api.home_db import DatabaseHome
import sqlite3


def test():
    db = DatabaseHome(path_to_db='test.db')
    # db.create_table_homes()
    print("Baza yaratildi")

    print("Bazaga malumotlarni qo`shamiz.")
    # db.add_data("Ijaraga", "Sergeli", 4, "Rasmlar", "BLABLABLALA", 400, "+998994376027")

    # db.delete_category("Ovqatlaraqwe")

    print("Bazadan malumotlarni chaqiramiz")
    db.delete_home(home_id=1)
    users = db.select_region("Sergeli")
    print(users)


test()
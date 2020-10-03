import sqlite3
from sqlite3.dbapi2 import Cursor


def table_exists(cursor: sqlite3.Cursor, table_name:str) -> bool:
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE TYPE = 'table' AND name = '{}'".format(table_name))
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False

def create_table(cursor: sqlite3.Cursor, table_name:str) -> None:
    cursor.execute("""CREATE TABLE '{}'(
                   user_name TEXT,
                   public_key TEXT
                   )
                   """.format(table_name))

def add_user(conn: sqlite3.Connection, cursor: sqlite3.Cursor, table_name:str, user_name:str, public_key:str):
    cursor.execute("""INSERT INTO '{}'
                   (user_name, public_key)
                   VALUES (?, ?)
                   """.format(table_name), (user_name, public_key))
    conn.commit()

def get_user(cursor: sqlite3.Cursor, table_name: str, user_name: str) -> list:
    cursor.execute("""
              SELECT * FROM '{}'
              WHERE user_name = '{}'
              """.format(table_name, user_name))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data 

def get_users(cursor: sqlite3.Cursor, table_name: str) -> list:
    cursor.execute("""
                   SELECT * FROM '{}'
                   """.format(table_name))
    data = []
    for row in cursor.fetchall():
        data.append(row)
    return data

def update_user(conn:sqlite3.Connection, cursor: sqlite3.Cursor, table_name: str, user_name: str, user_dict: dict) -> None:
    valid_keys = ["user_name", "public_key"]
    for key in user_dict.keys():
        if key not in valid_keys:
            raise Exception("Invalid field name.")
        else:
            if type(user_dict[key]) == str:
                stmt = """UPDATE '{}' SET {} = '{}'
                       WHERE user_name = '{}'""".format(table_name,
                                                      key,
                                                      user_dict[key],
                                                      user_name)
    cursor.execute(stmt)
    conn.commit()
    
    cursor.execute("""""".format())

def delete_user(conn: sqlite3.Connection , cursor: sqlite3.Cursor, table_name: str, user_name: str):
    cursor.execute("""
                   DELETE FROM '{}' WHERE user_name = '{}'
                   """.format(table_name, user_name))
    conn.commit()

def delete_all_users(conn: sqlite3.Connection , cursor: sqlite3.Cursor, table_name: str):
    cursor.execute("""
                   DELETE FROM '{}'
                   """.format(table_name))
    conn.commit()
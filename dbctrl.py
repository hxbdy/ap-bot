import sqlite3
import info
import pathlib

def create_db():
    pathlib.Path(info.DB).touch()

def create_table():
    conn = sqlite3.connect(info.DB)
    cur = conn.cursor()
    
    cur.execute(f'CREATE TABLE {info.TABLE_NAME}({",".join(info.COLUMNS)}, PRIMARY KEY({info.COLUMNS[0]}));')
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # DB作成
    # create_db()

    # DBにテーブル追加
    create_table()

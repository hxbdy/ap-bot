import sqlite3
import info
import pathlib

import info

def create_db():
    pathlib.Path(info.DB).touch()

def create_table():
    conn = sqlite3.connect(info.DB)
    cur = conn.cursor()
    
    cur.execute(f'CREATE TABLE {info.TABLE_NAME}({",".join(info.COLUMNS)}, PRIMARY KEY({info.COLUMNS[0]}));')
    
    conn.commit()
    cur.close()
    conn.close()

def get_random_question():
    """ランダムに1問取得"""
    conn = sqlite3.connect(info.DB)
    cur = conn.cursor()
    
    # テーブルを1つ決定
    cur.execute("SELECT NAME FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY RANDOM() LIMIT 1;")
    table_name = cur.fetchone()[0]


    # 一問決定
    # cur.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1;")
    cur.execute("SELECT * FROM q2023r05h_ap WHERE id=53;")
    row = cur.fetchone()
    
    cur.close()
    conn.close()

    
    print(table_name)
    print(row[info.ENUM_COLUMNS_ID])
    return row

if __name__ == "__main__":
    # DB作成
    # create_db()

    # DBにテーブル追加
    # create_table()

    get_random_question()

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

def get_random_exam_table_name():
    """ランダムに過去問テーブル決定"""
    conn = sqlite3.connect(info.DB)
    cur = conn.cursor()
    
    # テーブルを1つ決定
    cur.execute("SELECT NAME FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY RANDOM() LIMIT 1;")
    table_name = cur.fetchone()[0]
    
    cur.close()
    conn.close()

    return table_name

def get_random_question(table_name):
    """ランダムに1問取得"""
    conn = sqlite3.connect(info.DB)
    cur = conn.cursor()

    # 一問決定
    cur.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT 1;")
    row = cur.fetchone()
    
    cur.close()
    conn.close()

    return row

if __name__ == "__main__":
    # DB作成
    # create_db()

    # DBにテーブル追加
    create_table()

    # get_random_question()

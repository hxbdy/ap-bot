import sqlite3
import pandas as pd
import info

# id列用の文字列生成
ids = []
for i in range(1, info.QUESTION_NUM + 1):
    ids.append(f"{i}")


# 問題csv読み込み
with open(info.OUTPUT_BASE64_PATH, encoding='utf8') as file:
    question_base64 = file.read().splitlines()

# 解答カテゴリcsv読み込み
with open(info.INPUT_QUESTION_CAT_CSV_PATH, encoding='utf8') as file:
    answer_cat = file.read().splitlines()

# 解答csv読み込み
with open(info.INPUT_QUESTION_ANSWER_CSV_PATH, encoding='utf8') as file:
    answer = file.read().splitlines()

row = list(zip(ids, answer, answer_cat, question_base64))

df = pd.DataFrame(columns=info.COLUMNS)

# 挿入する列名一覧
col_name = ",".join(df.columns.values)

# プレースホルダ
replacement = ",".join(["?"] * len(df.columns))

sql = "INSERT OR REPLACE INTO {0} ( {1} ) VALUES ( {2} );".format(info.TABLE_NAME, col_name, replacement)

# 挿入
conn = sqlite3.connect(info.DB)
cur = conn.cursor()

cur.executemany(sql, row)
conn.commit()

cur.close()
conn.close()

DB = "./main.db"
EXAM_ID = "2023r05a_ap"

# 頭文字は数字以外の必要がある
TABLE_NAME = 'q' + EXAM_ID

# 1つ目は主キー
COLUMNS = ["id", "answer", "category", "question_base64"]

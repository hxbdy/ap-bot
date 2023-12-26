DB = "./main.db"
EXAM_ID = "2023r05a_ap"

# 問題数
QUESTION_NUM = 80

# 頭文字は数字以外の必要がある
TABLE_NAME = 'q' + EXAM_ID

# 1つ目は主キー
COLUMNS = ["id", "answer", "category", "question_base64"]

# jpgに変換する対象の問題pdfのパス
INPUT_PDF_PATH = f"./past_exam_question/{EXAM_ID}/question/pdf/{EXAM_ID}_am_qs.pdf"

# ページ分割済みPDF問題の画像フォルダへのパス
OUTPUT_JPG_PAGE_PATH = f"./past_exam_question/{EXAM_ID}/question/image/image_question/"
INPUT_JPG_PAGE_PATH = OUTPUT_JPG_PAGE_PATH + "*.jpg"

# 問題画像をbase64にエンコードした文字列をcsv出力するパス
OUTPUT_BASE64_PATH = f"./past_exam_question/{EXAM_ID}/question/csv/base64_question.csv"

# 問題csv読み込み
INPUT_QUESTION_CSV_PATH = f"./past_exam_question/{EXAM_ID}/question/csv/base64_question.csv"

# 解答カテゴリcsv読み込み
INPUT_QUESTION_CAT_CSV_PATH = f"./past_exam_question/{EXAM_ID}/answer/csv/category.csv"

# 解答csv読み込み
INPUT_QUESTION_ANSWER_CSV_PATH = f"./past_exam_question/{EXAM_ID}/answer/csv/answer.csv"

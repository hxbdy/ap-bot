import base64
import glob

# base64エンコード結果をリストに用意する
files = glob.glob("./past_exam_question/2023r05a_ap/question/image/image_question/*.jpg")
b64_ary = []
for img in files:
    with open(img,"rb") as imagefile:
        b64_ary.append(base64.b64encode(imagefile.read()).decode("ascii"))

# csv書き込み
csv_path = "./past_exam_question/2023r05a_ap/question/csv/base64_question.csv"
row = "\n".join(b64_ary)
with open(csv_path, 'w') as file:
    file.writelines(row)

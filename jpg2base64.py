import base64
import glob
import info

# base64エンコード結果をリストに用意する
files = glob.glob(info.INPUT_JPG_QUESTION_PATH)
b64_ary = []
for img in files:
    with open(img,"rb") as imagefile:
        b64_ary.append(base64.b64encode(imagefile.read()).decode("ascii"))

# csv書き込み
row = "\n".join(b64_ary)
with open(info.OUTPUT_BASE64_PATH, 'w') as file:
    file.writelines(row)

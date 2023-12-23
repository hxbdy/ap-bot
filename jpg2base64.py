import base64
import glob

files = glob.glob("./dst/*.jpg")

files = files[:2]

for img in files:
    with open(img,"rb") as imagefile:
        b64_string = base64.b64encode(imagefile.read())
        print(b64_string)
        print()



from pathlib import Path
from pdf2image import convert_from_path

# PDFファイルのパス
pdf_path = Path("./2023r05a_ap_am_qs.pdf")
#outputのファイルパス
img_path=Path("./image")

#この1文で変換されたjpegファイルが、imageホルダー内に作られます。
convert_from_path(pdf_path, output_folder=img_path,fmt='jpeg',output_file=pdf_path.stem)

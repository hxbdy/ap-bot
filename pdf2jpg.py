from pathlib import Path
from pdf2image import convert_from_path
import info

# PDFファイルのパス
pdf_path = Path(info.INPUT_PDF_PATH)

#outputのファイルパス
img_path = Path(info.OUTPUT_JPG_PAGE_PATH)

#この1文で変換されたjpegファイルが、imageホルダー内に作られます。
convert_from_path(pdf_path, output_folder=img_path, fmt='jpeg', output_file=pdf_path.stem)

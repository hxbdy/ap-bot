
import glob

import cv2

import json
import logging
import logging.config

from rich.logging import RichHandler
from rich.console import Console

import info

CONFIG = '''
{
    "version": 1,
    "disable_existing_loggers": false,
    "handlers": {
        "rich": {
            "class": "rich.logging.RichHandler",
            "level": "DEBUG",
            "rich_tracebacks": "True"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "rich"
        ]
    }
}
'''
logging.config.dictConfig(json.loads(CONFIG))
logger = logging.getLogger("search")
logger.setLevel(logging.DEBUG)


# PARAM

PREVIEW_ZOOM = 0.5                          # プレビュー表示倍率
RECIPROCAL_PREVIEW_ZOOM = 1 / PREVIEW_ZOOM  # 逆数

WINDOW_NAME = "sheet"
PREVIEW_WINDOW_NAME = "Pre-sheet"



x0 = y0 = x1 = y1 = 0
drag_flg = False
def mouse_coor(event, x, y, flags, param):
    global x0, y0, x1, y1, drag_flg, sheet, question_index
    if event == cv2.EVENT_LBUTTONDOWN:
        x0 = int(x * RECIPROCAL_PREVIEW_ZOOM)
        y0 = int(y * RECIPROCAL_PREVIEW_ZOOM)
        logger.debug(f"(x0, y0) = ({x}, {y})")
        drag_flg = True

    elif event == cv2.EVENT_LBUTTONUP:
        x1 = int(x * RECIPROCAL_PREVIEW_ZOOM)
        y1 = int(y * RECIPROCAL_PREVIEW_ZOOM)
        logger.debug(f"(x1, y1) = ({x}, {y})")
        drag_flg = False

        pre_sheet = cv2.copyTo(sheet, None)
        pre_sheet_resized = cv2.resize(pre_sheet[y0:y1, x0:x1], None, fx=PREVIEW_ZOOM, fy=PREVIEW_ZOOM)
        cv2.imwrite(info.OUTPUT_JPG_QUESTION_PATH + f"question_{question_index:02}.jpg", pre_sheet[y0:y1, x0:x1])
        cv2.imshow(PREVIEW_WINDOW_NAME, pre_sheet_resized)

    if drag_flg:
        x1 = int(x * RECIPROCAL_PREVIEW_ZOOM)
        y1 = int(y * RECIPROCAL_PREVIEW_ZOOM)
        pre_sheet = cv2.copyTo(sheet, None)
        cv2.rectangle(pre_sheet, (x0, y0), (x1, y1), (0, 255, 255), 2)
        cv2.imshow(WINDOW_NAME, cv2.resize(pre_sheet, None, fx=PREVIEW_ZOOM, fy=PREVIEW_ZOOM))


# 問題冊子読み込み
page_index = 0
files = glob.glob(info.INPUT_JPG_PAGE_PATH)
PAGE_MAX = len(files)
sheet = cv2.imread(files[page_index], cv2.IMREAD_GRAYSCALE)

# ウインドウ準備
cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.namedWindow(PREVIEW_WINDOW_NAME, cv2.WINDOW_NORMAL)

# マウスイベントのコールバックセット
cv2.setMouseCallback(WINDOW_NAME, mouse_coor)


question_index = 1
while True:
    logger.info("======================================================")
    logger.info(f"page index : {page_index}")
    logger.info(f"question index : {question_index}")
    logger.info("page     prev: q, next: e")
    logger.info("question prev: a, next: d")
    logger.info("quit: c")
    logger.info("======================================================")

    # 問題用紙表示
    sheet = cv2.imread(files[page_index], cv2.IMREAD_GRAYSCALE)

    # OpenCVの文字描画とサイズ指定 https://zenn.dev/waruby/articles/a6d831cbe7f8af
    cv2.putText(sheet, f"SELECT Q.{question_index}", (10, 50), cv2.FONT_HERSHEY_DUPLEX, 1.0, (0, 0, 0))
    cv2.imshow(WINDOW_NAME, cv2.resize(sheet, None, fx=PREVIEW_ZOOM, fy=PREVIEW_ZOOM))

    # 問題切り抜き表示
    pre_sheet = cv2.imread(info.OUTPUT_JPG_QUESTION_PATH + f"question_{question_index}.jpg", cv2.IMREAD_GRAYSCALE)
    if pre_sheet is not None:
        cv2.destroyWindow(PREVIEW_WINDOW_NAME)
        cv2.imshow(PREVIEW_WINDOW_NAME, cv2.resize(pre_sheet, None, fx=PREVIEW_ZOOM, fy=PREVIEW_ZOOM))

    
    
    # ページ操作, 問題数操作
    key = cv2.waitKey(0)
    if(chr(key) == 'q'):
        page_index -= 1
        if page_index < 0:
            page_index = 0
    elif(chr(key) == 'e'):
        page_index += 1
        if page_index >= PAGE_MAX:
            page_index = PAGE_MAX - 1
    elif(chr(key) == 'a'):
        question_index -= 1
        if question_index < 1:
            question_index = 1
    elif(chr(key) == 'd'):
        question_index += 1
        if question_index >= info.QUESTION_NUM:
            question_index = info.QUESTION_NUM
    elif(chr(key) == 'c'):
        break

cv2.destroyAllWindows()

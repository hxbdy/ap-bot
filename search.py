
import glob

import cv2
import numpy as np

import json
import logging
import logging.config

CONFIG = '''
{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "simple_format": {
            "format": "%(asctime)s [%(levelname)10s] %(message)s"
        }
    },
    "handlers": {
        "terminal": {
            "class": "logging.StreamHandler",
            "formatter": "simple_format",
            "level": "DEBUG"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "terminal"
        ]
    }
}
'''
logging.config.dictConfig(json.loads(CONFIG))
logger = logging.getLogger("search")
logger.setLevel(logging.DEBUG)


# PARAM
ACC_THR_E = 0.92     # 「エ」の一致率しきい値
ACC_THR_Q = 0.88     # 「問」の一致率しきい値



def get_location(image, templ, acc_thr):
    """imageからtemplを探す
    一致率がacc_thrを超えた座標をすべて返す"""
    result = cv2.matchTemplate(image, templ, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result > acc_thr)
    loc_list = list(zip(*loc[::-1]))
    logger.debug(f"loc_list = {loc_list}")
    return loc_list

def load_question_sheets():
    files = glob.glob("./image/*.jpg")
    for file in files:
        sheet = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        logger.info(f"{file}")
        yield sheet


# 選択肢エを読み込む
word_e = cv2.imread("./resrc/e.jpg", cv2.IMREAD_GRAYSCALE)
# 問を読み込む
word_q = cv2.imread("./resrc/q.jpg", cv2.IMREAD_GRAYSCALE)


# 問題用紙読み込み
question_number = 0
for sheet in load_question_sheets():
    # エの座標を取得
    loc_e_list = get_location(sheet, word_e, ACC_THR_E)
    for loc_e in loc_e_list:
        w,h = word_e.shape[::-1]
        cv2.rectangle(sheet, loc_e, (loc_e[0] + w, loc_e[1] + h), (0, 255, 255), 2)
    cv2.imshow("e", cv2.resize(sheet, None, fx=0.5, fy=0.5))
    cv2.waitKey(0)

    # 問の座標を取得
    loc_q_list = get_location(sheet, word_q, ACC_THR_Q)
    for loc_q in loc_q_list:
        w,h = word_q.shape[::-1]
        cv2.rectangle(sheet, loc_q, (loc_q[0] + w, loc_q[1] + h), (0, 255, 255), 2)
    cv2.imshow("q", cv2.resize(sheet, None, fx=0.5, fy=0.5))
    cv2.waitKey(0)


    # 一つも見つけられなかった
    if len(loc_q_list) == 0:
        logger.error("len(loc_q_list) == 0")
        continue

    # 検出した問題数と選択肢の数が一致しない
    # if len(loc_q_list) != len(loc_e_list):
    #     logger.error("question({0}) != choice({1})".format(len(loc_q_list), len(loc_e_list)))
    #     continue

    for i in range(len(loc_q_list)):
        loc_0 = loc_q_list[i]
        loc_1 = loc_e_list[i]

        x0 = loc_0[0] - 20
        y0 = loc_0[1] - 10

        x1 = 1300
        y1 = loc_1[1] + 80


        if (x0 > x1) or (y0 > y1):
            logger.error(f"invalid detection")
            break

        logger.debug(f"(x0, y0) = ({x0}, {y0})")
        logger.debug(f"(x1, y1) = ({x1}, {y1})")

        cv2.rectangle(sheet, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.imshow("tmp", cv2.resize(sheet, None, fx=0.5, fy=0.5))
        cv2.imshow("cut", sheet[y0:y1, x0:x1])
        cv2.waitKey(0)

        save_path = "./dst/result_{question_number}.jpg"
        logger.info(f"save {save_path}")
        cv2.imwrite(f"./dst/result_{i}.jpg", sheet[y0:y1, x0:x1])
        question_number += 1

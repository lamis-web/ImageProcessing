# Usage
# - python prepare_ProjSubjList.py /e/jchoi4/ImageData/C19/VIDA_20210701-01_C19_TK
# Input
# - VIDA results folder path
# Dependency
# - VidaDatasheet.xlsx
# Global Variable -----------------------------------------------------------
XLSX_PATH = r"E:\common\Taewon\oneDrive\OneDrive - University of Kansas Medical Center\VidaDataSheet.xlsx"
OUTPUT_PATH = "Data_to_send"
PATH_IN_B2 = f"/data4/common/ImageData"
# ---------------------------------------------------------------------------
import os
import sys
import argparse
import tarfile
from pathlib import Path
from datetime import datetime
from typing import List
from tqdm import tqdm
import pandas as pd


# parser = argparse.ArgumentParser(
#     description="Prepare ProjSubjList.in, Compressed zip of VIDA results and send it to the B2"
# )
# parser.add_argument(
#     "src", metavar="src", type=str, help="VIDA results source folder path"
# )
# args = parser.parse_args()
# VIDA_RESULTS_PATH = args.src
# OUTPUT_FOLDER = (
#     VIDA_RESULTS_PATH.split("/")[-1]
#     if VIDA_RESULTS_PATH.split("/")[-1] != ""
#     else VIDA_RESULTS_PATH.split("/")[-2]
# )


def _get_case_ids(VIDA_RESULTS_PATH: str) -> List[int]:
    try:
        case_ids = [int(case) for case in os.listdir(VIDA_RESULTS_PATH)]
    except:
        sys.exit("Error: Unexpected data included in source path")
    return case_ids


def _construct_ProjSubjList_in(XLSX_PATH: str):
    case_ids = [1377, 1388]
    df = pd.read_excel(XLSX_PATH, usecols="A:C,I")
    df = df.query('VidaCaseID in @case_ids')
    df['ImgDir'] = f'{PATH_IN_B2}/' +  df['Proj'] + '/' + df['VidaCaseID'].astype(str)
    df.rename(columns={"IN/EX": "Img"}, inplace=True)
    df.drop(columns=["VidaCaseID"], inplace=True)

    proj = df['Proj'].iloc[0]
    today = datetime.today().strftime("%Y%m%d")
    with open(f'{OUTPUT_PATH}/ProjSubjList.in.{today}_{proj}', 'w') as f:
        f.write(df)


# def _compress_vida_results(case_ids: List[int]):
#     with tarfile.open(f"{OUTPUT_PATH}/{OUTPUT_FOLDER}.tar.bz2", "w:bz2") as tar:
#         for case in tqdm(case_ids):
#             tar.add(Path(f"{VIDA_RESULTS_PATH}/{case}"), f"{OUTPUT_FOLDER}/{case}")


def _send_to_b2(ProjSubjList_in=None):
    pass

if __name__ == '__main__':
    _construct_ProjSubjList_in(XLSX_PATH)
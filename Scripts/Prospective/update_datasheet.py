# Usage
# - python update_datasheet.py {PROJ}
# Dependency
# - VidaDatasheet.xlsx
import os
import argparse
import pandas as pd
from openpyxl import load_workbook


XLSX_PATH = r"E:\common\Taewon\oneDrive\OneDrive - University of Kansas Medical Center\VidaDataSheet.xlsx"

# Create an argumnet parser
# parser = argparse.ArgumentParser(
#     description='Update VidaDataSheet.xlsx')
# parser.add_argument('proj', metavar='proj', type=str,
#                     help='Project Name')
# args = parser.parse_args()

# PROJ = args.proj


def _find_first_case_id_to_update(vida_datasheet_df):
    return int(vida_datasheet_df.iloc[-1]["VidaCaseID"])

def update_vida_datasheet(vida_datasheet_df, vida_dashboard_df):
    pass


if __name__ == '__main__':
    vida_datasheet_df = pd.read_excel(XLSX_PATH, sheet_name=0)
    vida_dashboard_df = pd.read_excel(XLSX_PATH, sheet_name=1)
    update_vida_datasheet(vida_datasheet_df, vida_dashboard_df)
    _find_first_case_id_to_update(vida_datasheet_df)
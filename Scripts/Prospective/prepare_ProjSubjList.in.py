# Usage
# - python prepare_ProjSubjList.in.py
# Dependency
# - VidaDatasheet.xlsx
# Global Variable -----------------------------------------------------------
XLSX_PATH = r"E:\common\Taewon\oneDrive\OneDrive - University of Kansas Medical Center\VidaDataSheet.xlsx"
# ---------------------------------------------------------------------------
import os
import argparse
import pandas as pd


df = pd.read_excel(XLSX_PATH)
print(df)
#%%
import camelot
import re
import logging
import glob
import PyPDF2 as pdf
import pandas as pd
from datetime import datetime
from pathlib import Path

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

COL_NAMES = [
    "AT-Number",
    "AT-Number self test",
    "ID-Number",
    "Manufacturer",
    "Test name",
    "Target antigen",
    "Cq <= 25",
    "Cq 25-30",
    "Cq >= 30",
    "Total sensitivity",
]


def extract_created_date(reader):
    # Get rid of `D:` prefix and timezone.
    stamp = reader.documentInfo["/CreationDate"]
    match = re.search("\d+", stamp)
    return datetime.strptime(match.group(), "%Y%m%d%H%M%S")


#%%
# Split pdf to single pages so we can read them one by one
log.info("Splitting .pdf to single files")
# match most recent .pdf
source = sorted(glob.glob("./data/raw/*.pdf"), reverse=True)[0]
from_file = pdf.PdfFileReader(source)
max_page_num = from_file.getNumPages()
date_created = extract_created_date(from_file)

#%%
# Skip introductory pages. Save only files containing tables
tab = 0
for page_num in range(0, max_page_num):
    log.info(f"Reading {source} page {page_num}")
    page = from_file.getPage(page_num)
    text = page.extractText().lower()
    # Skip until we occur tabelle 1 for first time
    tab = 2 if "tabelle 2:" in text else tab
    tab = 1 if "tabelle 1:" in text else tab
    if tab > 0:
        to_file = pdf.PdfFileWriter()
        dest = f"./data/interim/{date_created}_output_tab{tab}_{page_num:02d}.pdf"
        with open(dest, "wb") as file:
            to_file.insertPage(page)
            to_file.write(file)
            log.info(f"Wrote file: {dest}")

#%%
# Extract all tables 1 and tables 2 and merge to corresponding df
files = glob.glob(f"./data/interim/{date_created}*.pdf")
df_tab1 = pd.DataFrame()
df_tab2 = pd.DataFrame()
for file in sorted(files):
    log.info(f"Extracting Table from file {file}")
    table = camelot.read_pdf(file, flavor="stream", row_tol=10)
    if "tab1" in file.lower():
        df_tab1 = df_tab1.append(table[0].df)
    else:
        df_tab2 = df_tab2.append(table[0].df)

# Tab 2  has a missing column. Fix for alignment
df_tab2.insert(1, None, None)
# reset index
df_tab2.columns = range(df_tab2.shape[1])
df = df_tab1.append(df_tab2)


#%%
# Clean tables and write to .csv
df.columns = COL_NAMES
# Target Antigen col seems reliable. Valid entries are short!
df = df[(df["Target antigen"].str.len() > 0) & (df["Target antigen"].str.len() <= 4)]
dest = f"./data/final/{date_created}_table.csv"
df.to_csv(dest, index=False, encoding="utf-8")
log.info(f"Converted to csv: {dest}")

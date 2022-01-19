#%%
import json
import glob
import logging
import sys
import dateparser
import pandas as pd
from pathlib import Path
from flask import Flask, render_template

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

app = Flask(__name__)

VERSION = "v0.1.0"
DIR_DATA = "./data"
DIR_DATA_FINAL = DIR_DATA + "/final"


# Read most current file (use date as prefix)
try:
    file = sorted(glob.glob(f"{DIR_DATA_FINAL}/*.csv"), reverse=True)[0]
except IndexError:
    log.exception(f"\nMake sure there is a .csv file in {DIR_DATA_FINAL}/\n")
    sys.exit(1)
df = pd.read_csv(file)

DATE = dateparser.parse(Path(file).name[0:10]).date()
TITLE = "Covid-19 Antigen Test Comparison"
SUBTITLE = f"Data last updated on: {DATE}"

#%%

COL = df.columns
DATATABLES_CONFIG = [
    {"name": COL[0], "searchable": "false", "orderable": "false"},
    {"name": COL[1], "searchable": "false", "orderable": "false"},
    {"name": COL[2], "searchable": "false", "orderable": "false"},
    {"name": COL[3], "searchable": "true", "orderable": "true"},
    {"name": COL[4], "searchable": "true", "orderable": "true"},
    {"name": COL[5], "searchable": "false", "orderable": "true"},
    {"name": COL[6], "searchable": "false", "orderable": "true"},
    {"name": COL[7], "searchable": "false", "orderable": "true"},
    {"name": COL[8], "searchable": "false", "orderable": "true"},
    {"name": COL[9], "searchable": "false", "orderable": "true"},
]


@app.route("/")
def index():
    return render_template(
        "ajax_table.html",
        title=TITLE,
        subtitle=SUBTITLE,
        table_config=DATATABLES_CONFIG,
        version=VERSION,
    )


@app.route("/api/data")
def data():
    return {"data": json.loads(df.to_json(orient="records"))}


if __name__ == "__main__":
    app.run()

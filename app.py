import json
import glob
import logging
import sys
import dateparser
import subprocess
import os
import pandas as pd
from pathlib import Path
from flask import Flask, render_template

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

app = Flask(__name__)


def get_version() -> str:
    """get latest version from git tag"""
    try:
        r = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"], encoding="utf8"
        )
    except subprocess.CalledProcessError:
        return ""
    return r


MAIL = os.getenv("MAIL")
VERSION = get_version()
DIR_DATA = "./data"
DIR_DATA_FINAL = DIR_DATA + "/final"


# Read most current file (use date as filename prefix)
try:
    file = sorted(glob.glob(f"{DIR_DATA_FINAL}/*.csv"), reverse=True)[0]
except IndexError:
    log.exception(f"\nMake sure there is a .csv file in {DIR_DATA_FINAL}/\n")
    sys.exit(1)
df = pd.read_csv(file)

log.debug(f"File date to parse: {Path(file).name[0:8]}")
DATE = dateparser.parse(Path(file).name[0:8], ["%Y%m%d"]).date()
TITLE = "Corona Antigen Test Comparison"
SUBTITLE = f"Data last updated on: {DATE}" if DATE else ""

COL = df.columns
DATATABLES_CONFIG = [
    {"name": COL[0], "searchable": "false", "orderable": "false"},
    {"name": COL[1], "searchable": "false", "orderable": "false"},
    {"name": COL[2], "searchable": "false", "orderable": "false"},
    {"name": COL[3], "searchable": "true", "orderable": "true"},
    {"name": COL[4], "searchable": "true", "orderable": "true"},
    {"name": COL[5], "searchable": "false", "orderable": "true"},
    {"name": COL[6], "span": "Cq <=25", "searchable": "false", "orderable": "true"},
    {"name": COL[7], "span": "Cq 25-30", "searchable": "false", "orderable": "true"},
    {"name": COL[8], "span": "Cq >=30", "searchable": "false", "orderable": "true"},
    {"name": COL[9], "searchable": "false", "orderable": "true"},
]


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=TITLE,
        subtitle=SUBTITLE,
        table_config=DATATABLES_CONFIG,
        version=VERSION,
    )


@app.route("/about")
def about():
    return render_template("about.html", version=VERSION, mail=MAIL)


@app.route("/help")
def help():
    return render_template("help.html", version=VERSION)


@app.route("/api/data")
def data():
    return {"data": json.loads(df.to_json(orient="records"))}


if __name__ == "__main__":
    app.run()

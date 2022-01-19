#%%
import json
import glob
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)
# Read most current file (use date as prefix)
file = sorted(glob.glob("./data/final/*.csv"), reverse=True)[0]
df = pd.read_csv(file)

# %%
TITLE = "Covid-19 Antigen Test Comparison"
# will be unsed in the template to config DataTables
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

#%%


@app.route("/")
def index():
    return render_template(
        "ajax_table.html",
        title=TITLE,
        table_config=DATATABLES_CONFIG,
    )


@app.route("/api/data")
def data():
    return {"data": json.loads(df.to_json(orient="records"))}


if __name__ == "__main__":
    app.run()

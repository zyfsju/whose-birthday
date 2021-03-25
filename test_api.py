import os
import logging
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
    jsonify,
)
from flask_cors import CORS
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen
from pprint import pprint
import pandas as pd
import json
from datetime import datetime


pd.set_option("display.max_columns", None)


def get_clean_text(tag):
    return " ".join(tag.stripped_strings)


base = "https://en.wikipedia.org/w/"
URL = (
    base
    + "api.php?action=parse&prop=text&format=json&formatversion=2&page=Wikipedia:Database_reports/Birthday_today"
)
# url = "https://en.wikipedia.org/wiki/Wikipedia:Database_reports/Birthday_today"

STATIC_FOLDER = "data"
MATH_FILE = f"{STATIC_FOLDER}/mathematician.csv"
TODAY = datetime.now().strftime("%Y-%m-%d")


def get_raw_table(cache=True):
    """
        Extracts the birthday table from the wikipedia page.
    """
    with urlopen(URL) as response:
        try:
            res = json.loads(response.read().decode())
        except:
            return
    html = res.get("parse", {}).get("text")
    soup = BeautifulSoup(html, "html.parser")
    p_tags = soup.find_all("p")
    updated_at = "Unknown"
    for p in p_tags:
        text = get_clean_text(p)
        if "Last update" in text:
            updated_at = text.split("update:")[1].strip()[:10]
            break
    file_path = f"{STATIC_FOLDER}/{updated_at}.csv"
    if os.path.isfile(file_path):
        return pd.read_csv(file_path)
    table = soup.find("table")
    headers = []
    for header in table.find_all("th"):
        headers.append(get_clean_text(header))
    df = pd.DataFrame(columns=headers, index=range(8000))
    row_marker = 0
    for row in table.find_all("tr"):
        column_marker = 0
        columns = row.find_all("td")
        for column in columns:
            df.iat[row_marker, column_marker] = get_clean_text(column)
            column_marker += 1
        row_marker += 1
    df.dropna(axis=0, how="all", inplace=True)
    df["UpdatedAt"] = updated_at
    if cache:
        df.to_csv(file_path, index=False)
    return df


def filter_table(df, keyword="mathematician", output_file=MATH_FILE, to_console=False):
    """
        Filters a table by keyword, and writes to disk.
    """
    filtered = []
    for col in df.columns:
        filtered.append(df[df[col].map(str).str.contains(keyword)])
    if filtered:
        filtered = pd.concat(filtered)
        filtered.drop_duplicates(inplace=True)
        mode = "a" if os.path.isfile(output_file) else "w"
        filtered.to_csv(output_file, index=False, mode=mode)
    if to_console:
        to_show = filtered[["Person", "Born", "description"]].set_index("Person")
        to_show.loc[:, "description"] = to_show["description"].map(lambda x: x[:40])
        pprint(to_show)
    return filtered


app = Flask(__name__, static_folder=STATIC_FOLDER)
CORS(app)


@app.route("/")
def index():
    return redirect(f"/mathematician/{TODAY}")


@app.route("/<keyword>/<date>")
def get_daily_data(keyword="mathematician", date=TODAY):
    DAILY_DATA = f"{STATIC_FOLDER}/{date}.csv"
    if os.path.isfile(DAILY_DATA):
        if not os.path.isfile(MATH_FILE):
            df = pd.read_csv(DAILY_DATA)
            table = filter_table(df, keyword)
        else:
            table = pd.read_csv(MATH_FILE)
            table = table[table["UpdatedAt"] == date]
    else:
        df = get_raw_table()
        updated_at = df.loc[0, "UpdatedAt"]
        if updated_at != date:
            return jsonify([])
        if not os.path.isfile(MATH_FILE):
            table = filter_table(df, keyword)
        else:
            table = pd.read_csv(MATH_FILE)
            table = table[table["UpdatedAt"] == updated_at]
            if len(table) == 0:
                table = filter_table(df, keyword)
    return jsonify(json.loads(table.to_json(orient="records")))


if __name__ == "__main__":
    app.run(debug=True)

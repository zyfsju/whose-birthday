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
# URL =base + "api.php?action=query&prop=revisions&page=Wikipedia:Database_reports/Birthday_today&rvprop=timestamp|user|comment&rvslots=main&formatversion=2"
# url = "https://en.wikipedia.org/wiki/Wikipedia:Database_reports/Birthday_today"
URL = base + "api.php?action=query&prop=revisions&page=Wikipedia:Database_reports/Birthday_today&formatversion=2&redirects=1&rvprop=timestamp"

STATIC_FOLDER = "data"
MATH_FILE = f"{STATIC_FOLDER}/mathematician.csv"
TODAY = datetime.now().strftime("%Y%m%d")
DAILY_DATA = f"{STATIC_FOLDER}/{TODAY}.csv"


with urlopen(URL) as response:
    # res = json.loads(response.read().decode())
    res = response.read().decode()
# html = res.get("parse", {}).get("text")
# soup = BeautifulSoup(html, "html.parser")
# p_tags = soup.find_all("p")
# for p in p_tags:
#     text = get_clean_text(p)
#     if "Last update" in text:
#         date = text.split("update:")[1].strip()
#         updated_at = datetime.strptime(date[:10], "%Y-%m-%d")
#         break
pprint(res)



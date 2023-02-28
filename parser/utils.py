import re
import urllib.request
from datetime import datetime
from time import sleep
from django.template.defaultfilters import slugify
import feedparser
import mysql.connector
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

from cleantext import clean, fix_bad_unicode
from loguru import logger
import os

config = load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR, 'parser/habr_csv/')


def connect_to_db():
    connection = mysql.connector.connect(
                database=os.environ["DATABASE"],
                host=os.environ["DB_HOST"],
                user=os.environ["DB_USER"],
                password=os.environ["DB_PASSWORD"])

    cursor = connection.cursor()

    return connection, cursor

def remove_unwanted(text) -> str:
    text = clean(text,  no_emoji=True)
    text = fix_bad_unicode(text)

    return text


def download_title_img(img_url) -> str:
    image = urllib.request.urlretrieve(str(img_url), "")

    return image

def download_multiple_images(images) -> str or list:
    images_downloaded = []
    for image in images:
        image_downloaded = download_title_img(image)
        images_downloaded.append(image_downloaded)
    return images_downloaded


def author_profile():
    author = "nicko_b"
    try:
        connection, cursor = connect_to_db()
        query = f"SELECT id FROM main_profile WHERE user='{author}'"
        cursor.execute(query)
        result = cursor.fetchall()

        return result[0][0]

    except NameError as n:
        n("No Profile Nicko_B")
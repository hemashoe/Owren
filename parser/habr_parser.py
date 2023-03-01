import re
from datetime import datetime
from typing import Any, Union

import feedparser
import pandas as pd
from slugify import slugify
from loguru import logger
from newspaper import Article
from utils import (DATA_DIR, author_profile, check_duplication, connect_to_db,
            remove_unwanted, download_title_img, download_multiple_images)

FILE_NAME = str(DATA_DIR +  "habr_data" + datetime.now().strftime("%m-%d_%H:%M") + ".csv")

def parse_posts() -> list:
    try:
        rss_data = feedparser.parse('https://habr.com/ru/rss/all/all/?fl=ru')
        posts_count = len(rss_data.entries)
        posts_parsed = []

        for post in range(posts_count):
            post_content = rss_data.entries[post]
            post_id = re.search(r'post/(\d+)/', post_content.guid).group(1)

            post_parsed: dict[str, Union[str, Any]] = {
                'post_id': post_id,
                'title': post_content.title,
                'link': post_content.guid,
            }
            posts_parsed.append(post_parsed)
        return posts_parsed

    except Exception:
        print("Unable to parse habr.com")


def get_article(posts_parsed : list ) -> None:
    try:
        data_parsed = []

        for post in posts_parsed:
            article =Article(post['link'])
            article.download() 
            article.parse()
            images = ["" + img for img in article.images]

            data = {
                    'post_id': post['post_id'],
                    'title': post['title'],
                    'description': article.meta_description,
                    'source_link': article.url,
                    'body': article.text,
                    'image': article.top_image,
                    'images': images,
            }
            data_parsed.append(data)

        dataframe = pd.DataFrame(data_parsed)
        dataframe.to_csv(FILE_NAME, sep="'", header=True, index=True,index_label="post_id" )

        return data_parsed

    except NameError as n:
        raise n("Unable to parse habr.com")


def update_db(data_parsed):
    connection, cursor = connect_to_db()
    author = author_profile()

    for data in data_parsed:
        check_for_dublicate = check_duplication(data['post_id'])

        if check_for_dublicate==False:
            try:
                body_text = remove_unwanted(data['body'])
                slug = slugify(data['title'])
                description_text = remove_unwanted(data['description'])
                title_img = download_title_img(data['image'], data['post_id'])
                download_multiple_images(data['images'], data['post_id'])

                query = f"INSERT INTO main_post (title, slug, source_link, source_id, description, body, title_image, published, author_id)" \
                        f'VALUES ("{data["title"]}", "{slug}", "{data["source_link"]}", "{data["post_id"]}", "{str(description_text[0])}", "{str(body_text[0])}", "{title_img}", "0", "{author}")'
                cursor.execute(query)
                connection.commit()
                print(f"Post {data['post_id']} added to database")
                    
            except NameError as n:

                raise n(f"Unable to update db. Problem in {data['post_id']}")
        else:
            pass


def main():
    try:
        print("Starting To Parse")
        posts_parsed = parse_posts()
        data_parsed=get_article(posts_parsed)
        update_db(data_parsed)
        print("Finished")
    
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
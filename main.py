import json
import os

import mysql.connector
import requests
from bs4 import BeautifulSoup

database_connection = mysql.connector.connect(
    host=os.getenv("host"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    database=os.getenv("database")
)
database_cursor = database_connection.cursor()
base_url = "https://vipergirls.to"
with open("links_to_img_urls.json", "r") as data_file:
    links_to_scrape = json.load(data_file)
next_page_url = thread_url = links_to_scrape["threads"][0]  # f"{base_url}/threads/5842541-VlXEN-Photo-Collection"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
data_from_pages = {}
# try:
#     with open("data.json", "r") as data_file:
#         data_from_pages = json.load(data_file)
# except FileNotFoundError:
#     with open("data.json", "w") as data_file:
#         json.dump(data_from_pages, data_file, indent=4)
# try:
#     next_page_url = data_from_pages.get(thread_url).get("next_url_to_visit")
# except AttributeError:
#     data_from_pages[thread_url] = {}
while next_page_url:
    res = requests.get(next_page_url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    post_contents = [
        {
            "title": post.select_one("div > font").get_text(),
            "image_links":
                {
                    "image_link": post.select_one("a").get("href"),
                    "preview_image_link": post.select_one("a").select_one("img").get("src")
                }
        } for post in soup.select("#postlist > ol#posts > li.postcontainer blockquote.postcontent.restore")
        if post.select_one("div > font") and post.select("a > img")]
    # data_from_pages[thread_url][next_page_url] = post_contents
    next_page_url_tag = soup.select_one("#pagination_bottom .prev_next > a[title~='Next']")
    if next_page_url_tag:
        next_page_url = f"{base_url}/{next_page_url_tag.get('href')}"
    else:
        break
    print(next_page_url)
    # data_from_pages[thread_url]["next_url_to_visit"] = next_page_url
    # with open("data.json", "r") as data_file:
    #     data = json.load(data_file)
    # data.update(data_from_pages)
    # with open("data.json", "w") as data_file:
    #     json.dump(data, data_file, indent=4)

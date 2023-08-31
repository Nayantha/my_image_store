import json

import requests
from bs4 import BeautifulSoup

base_url = "https://vipergirls.to"
next_page_url = f"{base_url}/threads/5842541-VlXEN-Photo-Collection"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
data_from_pages = {}
try:
    with open("data.json", "r") as data_file:
        data_from_pages = json.load(data_file)
except FileNotFoundError:
    with open("data.json", "w") as data_file:
        json.dump(data_from_pages, data_file, indent=4)
last_url_visited_in_file = data_from_pages.get("next_url_to_visit")
if last_url_visited_in_file:
    next_page_url = last_url_visited_in_file
while next_page_url:
    res = requests.get(next_page_url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    post_contents = [
        {
            "title": post.select_one("div > font").get_text(),
            "image_links": [
                a_tag.get("href") for a_tag in post.select("a") if a_tag.select("img")
            ]
        } for post in soup.select("#postlist > ol#posts > li.postcontainer blockquote.postcontent.restore")
        if post.select_one("div > font") and post.select("a > img")]
    data_from_pages[next_page_url] = post_contents
    next_page_url_tag = soup.select_one("#pagination_bottom .prev_next > a[title~='Next']")
    data_from_pages["next_url_to_visit"] = next_page_url
    with open("data.json", "r") as data_file:
        data = json.load(data_file)
    data.update(data_from_pages)
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

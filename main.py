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
    new_data = {
        next_page_url: post_contents
    }
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            json.dump(new_data, data_file, indent=4)
    else:
        data.update(new_data)
        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)
    next_page_url = soup.select_one("#pagination_bottom .prev_next > a")
    next_page_url = f"{base_url}/{next_page_url.get('href')}" if next_page_url else None

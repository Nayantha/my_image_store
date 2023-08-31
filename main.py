import requests
from bs4 import BeautifulSoup
from rich.pretty import pprint

base_url = "https://vipergirls.to"
threat_url = f"{base_url}/threads/5842541-VlXEN-Photo-Collection"
# save from base url
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(threat_url, headers=headers)
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
# pprint(post_contents)
next_page = soup.select_one("#pagination_bottom .prev_next > a")
next_page = f"{base_url}/{next_page.get('href')}" if next_page else None
# save data from current url
# repeat until meet end

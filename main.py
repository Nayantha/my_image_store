import requests
from bs4 import BeautifulSoup

base_url = "https://vipergirls.to/threads/5842541-VlXEN-Photo-Collection"
# save from base url
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(base_url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser")
post_contents = soup.select("#postlist > ol#posts > .postcontent ")
print(post_contents)
current_page = 2
new_url = f"{base_url}/?page={current_page}"
# save data from current url
# repeat until meet end

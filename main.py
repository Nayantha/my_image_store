import requests

base_url = "https://vipergirls.to/threads/5842541-VlXEN-Photo-Collection"
# save from base url
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
res = requests.get(base_url, headers=headers)
res.raise_for_status()
current_page = 2
new_url = f"{base_url}/?page={current_page}"
# save data from current url
# repeat until meet end

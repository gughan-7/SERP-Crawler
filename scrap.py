import json
import csv
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import re

def scrape_google_results(query, num_pages):
    query = urllib.parse.quote_plus(query)
    results = []

    for page in range(num_pages):
        start = page * 10
        url = f"https://www.google.com/search?q={query}&start={start}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        session = HTMLSession()
        response = session.get(url)
        #regex to filter out only links that lead to a youtube channel
        reg = "^https?:\/\/(www\.)?youtube\.com\/(channel\/UC[\w-]{21}[AQgw]|(c\/|user\/)?[\w-]+)$"
        links = list(response.html.absolute_links)
        p = re.compile(reg)
        for i in links:
            l = p.match(i)
            if l:
                results.append({"url": i})

    return results

query = "site:youtube.com channels"
num_pages = 20

results = scrape_google_results(query, num_pages)

print(results)

#write info onto csv
csv_filename = "serp.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

#write info onto json
json_filename = "serp.json"
with open(json_filename, "w", encoding="utf-8") as jsonfile:
    json.dump(results, jsonfile, ensure_ascii=False, indent=4)


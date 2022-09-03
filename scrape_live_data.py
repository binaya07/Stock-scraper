import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
LIVE_STOCK_PRICE_URL = "https://www.sharesansar.com/live-trading"
COLUMN_INDX_MAP = {0: "sn", 1: "stock", 2: "ltp", 3: "point_change",
                   4: "percent_change", 5: "open", 6: "high", 7: "low", 8: "volume", 9: "prev_close", 10: "detail_link"}

# Get html response
r = requests.get(url=LIVE_STOCK_PRICE_URL)

# Parse html and get live data
parsed_data = []

soup = BeautifulSoup(r.content, "html5lib")
table = soup.find("table", attrs={"id": "headFixed"})
table_body = table.find("tbody")

for row in table_body.findAll("tr"):
    columns = row.findAll("td")
    parsed_row = {}
    for i, column in enumerate(columns):
        if i == 1:
            parsed_row[COLUMN_INDX_MAP.get(i)] = str(column.a.text).strip()
            parsed_row[COLUMN_INDX_MAP.get(10)] = str(column.a["href"]).strip()
        else:
            parsed_row[COLUMN_INDX_MAP.get(i)] = str(column.text).strip()
    parsed_data.append(parsed_row)

print(len(parsed_data))
print(parsed_data[218])


filename = "stock_price_sep_3_2022_sharesansar.csv"
with open(filename, "w", newline="") as f:
    w = csv.DictWriter(f,COLUMN_INDX_MAP.values())
    w.writeheader()
    for data in parsed_data:
        w.writerow(data)

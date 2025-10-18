import sys
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrapeTablet(url, writer, parameters):
  page = urlopen(url)
  html = page.read().decode("utf-8")
  soup = BeautifulSoup(html, "html.parser")

  data = {param: "N/A" for param in parameters}
  data["URL"] = url

  name_tag = soup.select_one("h1")
  if name_tag:
    data["Name"] = name_tag.get_text(strip=True)

  price_container = soup.select_one("span.VersionOfferPrice")
  if price_container:
    currency = price_container.select_one("span.VersionPriceSymbol")
    whole = price_container.select_one("span.VersionPriceWhole")
    decimal = price_container.select_one("span.VersionPriceDecimal")

    currency_text = currency.get_text(strip=True) if currency else ""
    whole_text = whole.get_text(strip=True) if whole else ""
    decimal_text = decimal.get_text(strip=True) if decimal else ""
    data["Price"] = currency_text + whole_text + decimal_text


  rows = soup.select("#tab-dimensions tr")
  for row in rows:
    tds = row.find_all("td")
    if len(tds) < 2:
      continue

    header = tds[0].find("span", class_="Header")
    if not header:
      continue

    header_text = header.get_text(strip=True)
    value_text = tds[1].get_text(strip=True)

    if header_text in data:
      data[header_text] = value_text if value_text else "N/A"

  writer.writerow([data[param] for param in parameters])


def scrapeTablets():

  writer = csv.writer(sys.stdout, delimiter="\t")
  parameters = [
    "URL",
    "Name",
    "Price",
    "Processor",
    "Storage",
    "RAM",
    "Operating System",
    "Screen size",
    "Resolution",
    "Tablet Height",
    "Rear camera",
    "Colour",
  ]

  while True:
    try:
      url = input().strip()
    except EOFError:
      break

    if not url:
      break

    scrapeTablet(url, writer, parameters)

if __name__ == "__main__":
    scrapeTablets()

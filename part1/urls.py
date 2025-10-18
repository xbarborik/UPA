from bs4 import BeautifulSoup
from urllib.request import urlopen

def getTabletUrls(number_of_products_to_scrape = 150):
  pageNumber = 1
  number_of_urls_acquired = 0
  urls = set()

  while number_of_urls_acquired < number_of_products_to_scrape:
    url = "https://www.laptopsdirect.co.uk/ct/tablet-pcs-and-e-readers/tablets?pageNumber=" + str(pageNumber)
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    product_list = soup.select_one("#productList")
    a_tags = product_list.find_all("a", class_="offerboxtitle")

    for a_tag in a_tags:
      url = "https://www.laptopsdirect.co.uk/" + a_tag["href"]
      if url in urls:
        continue
      print(url)
      number_of_urls_acquired += 1
      urls.add(url)
      if (number_of_urls_acquired) >= number_of_products_to_scrape:
        break

    pageNumber += 1

if __name__ == "__main__":
  getTabletUrls()
  
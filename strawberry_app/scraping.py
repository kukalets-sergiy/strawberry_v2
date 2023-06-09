from bs4 import BeautifulSoup
import requests

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537"
                  ".36"
}


def collect_products(url="https://www.olx.ua/d/uk/dom-i-sad/q-%D1%81%D0%B0%D0%B4%D0%B6%D0%B0%D0%BD%D1%86%D1%96-%D0%BF"
                         "%D0%BE%D0%BB%D1%83%D0%BD%D0%B8%D1%86%D1%96/?currency=UAH&search%5Bfilter_enum_state%5D%5B0%5D"
                         "=new"):
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    products = ()
    total_products = 0
    pagination_div = soup.find('div', class_='css-4mw0p4')
    if pagination_div:
        pagination_items = pagination_div.find_all('li', class_='pagination-item css-ps94ux')
        if pagination_items:
            page_count = int(pagination_items[-1].text.strip())
            print("[INFO] Collecting products from the first page...")
            print(f"[INFO] Page count: {page_count}...")
            for page in range(1, page_count+1):
                print(f"[INFO] handle {page} page...")
                url = f"https://www.olx.ua/d/uk/dom-i-sad/q-%D1%81%D0%B0%D0%B4%D0%B6%D0%B0%D0%BD%D1%86%D1%96-%D0%BF%D" \
                      f"0%BE%D0%BB%D1%83%D0%BD%D0%B8%D1%86%D1%96/?currency=UAH&page={page}&search%5Bfilter_enum_state" \
                      f"%5D%5B0%5D=new"
                response = requests.get(url=url, headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')
                items = soup.find_all('div', class_='css-1sw7q4x')
                for item in items:
                    div = item.find('div', class_='css-u2ayx9')
                    if div is None:
                        continue
                    title = div.find('h6', class_='css-16v5mdi er34gjf0').text.strip()
                    link = "https://www.olx.ua" + item.find('a', class_='css-rc5s2u').get('href').strip()
                    try:
                        price = div.find('p', class_='css-10b0gli er34gjf0').text.strip()
                    except AttributeError:
                        price = 'the price is absent'
                    print(title)
                    print(link)
                    print(price)
                    total_products += 1
                    products += ({
                                     "title": title,
                                     "link": link,
                                     "price": price,
                                 },)
                    print(f"[INFO] Total products collected: {total_products}")
        return products


collect_products()


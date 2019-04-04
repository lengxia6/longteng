import requests
from bs4 import BeautifulSoup


def get_orders(url):
    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    h = bs.select('#billboard > div.billboard-hd > h2')[0]
    t = h.contents[0]
    orders = bs.select('#billboard > div.billboard-bd > table')[0]
    urls = []
    for order in orders.find_all('a'):
        urls.append((order['href'],order.string))
    return t, urls


def get_contens(url):

    res = requests.get(url)
    bs = BeautifulSoup(res.text, 'lxml')
    c = bs.select('#link-report')[0]

    return(c.text)


if __name__ == '__main__':

    url = 'https://movie.douban.com/'
    t, urls = get_orders(url)
    print(t)
    for url, name in urls:
        print(name)
        print(get_contens(url))

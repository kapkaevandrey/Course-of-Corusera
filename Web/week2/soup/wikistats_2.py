from bs4 import BeautifulSoup
import os
from wikistats import parse
import unittest



def build_bridge(path, start_page, end_page):
    with open(os.path.join(path, start_page)) as page:
        pass


with open("wiki/Stone_Age", encoding="utf-8") as html:
    soup = BeautifulSoup(html, "lxml")
    for link in soup.find_all("a"):
        print(link.get('href'))


def get_statistics(path, start_page, end_page):
    pass

path = os.path.join("wiki", os.path.dirname("wiki"))
# print(os.listdir('wiki'))
print(path)
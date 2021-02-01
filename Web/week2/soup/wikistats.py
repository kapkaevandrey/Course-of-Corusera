from bs4 import BeautifulSoup
import unittest


def count_image(body: object, width: int = 200):
    images = body.find_all('img')
    counter = 0
    for image in images:
        if image.has_attr("width") and int(image["width"]) >= width:
            counter += 1
    return counter


def count_tag(body: object, tag_name: str = "h", chars: list = []):
    tag_list = [f"{tag_name}{i}" for i in range(0, 7)]
    tag_list.insert(0, tag_name)
    htags = body.find_all(tag_list)
    counter = 0
    for tag in htags:
        if tag.text[0] in chars:
            counter += 1
    return counter


def count_chain(body: object, tag_name: str = "a"):
    aparents = [0]
    list_a = body.find_all(tag_name)
    current_parent = list_a[0].parent
    parent_index = 0
    for a in list_a:
        if a.parent is current_parent and (parent_index == 0 or a.previousSibling.name == 'a' or a.previousSibling.previousSibling.name == 'a'):
            aparents[parent_index] += 1
            current_parent = a.parent
        else:
            aparents.append(1)
            parent_index += 1
            current_parent = a.parent
    return max(aparents)

def find_list(body: object):
    _list = [i for i in body.find_all(["ol", "ul"]) if i.find_parent(["ol", "ul"]) is None]
    return (len(_list))


def parse(path_to_file):
    imgs = headers = linkslen = lists = 0
    with open(path_to_file, encoding="utf-8") as html:
        # тело запроса
        soup = BeautifulSoup(html, "lxml").find('div', id="bodyContent")
        # поиск изображений
        imgs = count_image(soup, width=200)
        # поиск тегов h# и выделение контента
        headers = count_tag(soup, tag_name="h", chars=['T', 'E', 'C'])
        # поиск последовательностей по всем тегам ссылок
        linkslen = count_chain(soup, tag_name="a")
        # поиск количества спсисков не вложенных в другие списки
        lists = find_list(soup)

class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()

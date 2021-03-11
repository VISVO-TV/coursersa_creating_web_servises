from bs4 import BeautifulSoup
import unittest


def parse(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('div', id='bodyContent')

    imgs = body.find_all('img') # 1. изображения > 200px
    counter_img = 0
    for img in imgs:
        try:
            if int(img.get('width')) > 199:
                counter_img += 1
        except TypeError:
            pass

    hs = body.select('h1, h2, h3, h4, h5, h6') # 2. заголовки с заглавной 'ETC'
    counter_h = 0
    for h in hs:
        if h.text[0] in 'ETC':
            counter_h += 1

    links = body.find_all('a') # 3. ссылки подряд
    counter_link = 0
    for link in links:
        counter = 1
        while True:
            next_tag = link.find_next_sibling()
            # print(str(next_tag)[:2])
            if str(next_tag)[:2] in '<a ':
                counter += 1
                link = next_tag
                if counter_link < counter:
                    counter_link = counter

            else:
                break

    uls = body.select('ol, ul') # 4. невложенные списки
    counter_ul = 0
    for ul in uls:
        if ul.find_parents('ul') == [] and ul.find_parents('ol') == []:
            counter_ul +=1

    return [counter_img, counter_h, counter_link, counter_ul]


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

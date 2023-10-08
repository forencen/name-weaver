import requests
from lxml import etree

from sqlite_helper import SQLiteDB


class FetchWordFormKX:

    def __init__(self):
        self.base_url = 'https://www.yw11.com'
        self.db = SQLiteDB('kangxi.db')

    def _fetch_word_from_bi_hua_next_page(self, html, fetched_url):
        next_path = html.xpath('/html/body/div[5]/div/div[1]/div[3]/ul/li[@class="page-prev"]/a/@href')
        if not next_path:
            return None
        next_path = next_path[0]
        if next_path in fetched_url:
            return None
        fetched_url.add(next_path)
        return self.base_url + next_path

    def _fetch_word_from_bi_hua_save_data(self, html, bi_hua):
        words = html.xpath('/html/body/div[5]/div/div[1]/div[2]/div/ul/li/a')
        data = []
        for word in words:
            uri = word.xpath('@href')
            word_ping_yin = word.xpath('em/text()')
            word_zi = word.xpath('span/text()')
            if not word_zi:
                continue
            data.append({
                'word': word_zi[0],
                'ping_yin': word_ping_yin[0] if word_ping_yin else '',
                'uri': uri[0] if uri else '',
                'bi_hua': bi_hua,
            })
        self.db.insert_multiple_data('word', data)

    def fetch_word_from_bi_hua(self, bi_hua):
        _uri = '/zidian/bihua/' + str(bi_hua) + '/'
        url = self.base_url + _uri
        fetched_url = {_uri, _uri + '1/'}
        while True:
            res = requests.get(url)
            html = etree.HTML(res.text)
            self._fetch_word_from_bi_hua_save_data(html, bi_hua)
            url = self._fetch_word_from_bi_hua_next_page(html, fetched_url)
            if not url:
                break


if __name__ == '__main__':
    f = FetchWordFormKX()
    for i in range(1, 31):
        if i in (12, 13):
            continue
        f.fetch_word_from_bi_hua(i)
    f.db.close()

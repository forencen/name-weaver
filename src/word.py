import requests
from lxml import etree

from sqlite_helper import SQLiteDB

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
}

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

    def _fetch_word_from_bu_shou(self, pian_pang_url, pian_pang):
        pass


    def fetch_word_from_bu_shou(self):
        url = 'https://www.yw11.com/zidian/bushou_index/'
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        bu_shou_div = html.xpath('/html/body/div[5]/div/div[1]/div[1]/div')
        for div in bu_shou_div:
            bu_shou_li = div.xpath('/ul/li')
            for li in bu_shou_li:
                url = li.xpath('a/@href')
                span = li.xpath('a/span/text()')


if __name__ == '__main__':
    f = FetchWordFormKX()
    f.fetch_word_from_bu_shou()
    f.db.close()

# -*- coding: utf-8 -*-
from w2a.lib.searcher.search_engine import SearchEngine


class Google(SearchEngine):
    """docstring for Google"""

    def __init__(self, keyworld, limit, delay):
        super().__init__('http://www.google.com/', keyworld, limit, delay)
        self.name = 'www.google.com'
        self.info = 'Google search engine'

    def uri_creater(self):
        return "http://www.google.com/search?&q=%s&start=%d&num=100&filter=1" % (self.keyworld, self.count)

    def get_data(self, data):
        return data.split('<div class="g">', 1)[1].rsplit('</div></ol></div></div></div>', 1)[0].split('<div class="g">')

    def spliter(self, info):
        s = {}
        s['url'] = info.split('url?q=', 1)

        if len(s['url']) > 1:
            s['url'] = s['url'][1].split('&', 1)[0]
        else:
            s['url'] = info.split('url=', 1)[1].split('&', 1)[0]

        s['data'] = info.split('<span class="st"', 1)[1].rsplit('</span>', 1)[0].replace('<b>', '').replace(
            '</b>', '').replace('<br>  ', '').replace('\n', '').strip()

        return s

    def has_next(self, data):
        if data.find(">Next</span>") == -1 and data.find(">Tiếp</span>") == -1:
            return False
        return True

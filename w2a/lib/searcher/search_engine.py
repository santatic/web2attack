# -*- coding: utf-8 -*-
from requests import get
from time import sleep
from re import findall, search
from urllib.parse import quote_plus

from w2a.lib.thread import Thread
from w2a.config import CONFIG
from w2a.core import printer


class SearchEngine(Thread):
    """docstring for SearchEngine"""

    name = 'VinaKid'

    def __init__(self, host, keyworld, limit, delay):
        super().__init__()
        self.keyworld = quote_plus(keyworld)
        self.limit = limit
        self.delay = delay
        self.count = 0
        self.content = []
        self.step = 10

    def run(self):
        while True:
            printer.print_line('\t{0:<25} {1:d}'.format(self.name, self.count))
            uri = self.uri_creater()

            if not self.has_next(self.do_search(uri)):
                break
            if self.count <= 1:
                break

            self.count += self.step
            if self.count >= self.limit:
                break

            sleep(self.delay)

    def do_search(self, uri):
        data = get(uri).text

        # print("-----------data : %s" % data)
        if data != '':
            try:
                content = self.get_data(data)
            except Exception as e:
                printer.print_error('%s : Nothing to do !' % self.name)
                return ''

            self.do_split(content)
        return data

    def do_split(self, content):
        ifl = []
        for i in content:
            try:
                ifl.append(self.spliter(i.strip()))
            except Exception as e:
                printer.print_error(
                    '%s Error : %s\ncontent: %s' % (self.name, e, i))

        self.content += ifl

        if self.step > len(ifl):
            return False
        return True

    def uri_creater(self):
        return None

    def has_next(self, i):
        pass

    def spliter(self, i):
        pass

    def get_data(self, data):
        pass

# -*- coding: utf-8 -*-

from requests import get
from time import sleep
import re

from urllib.parse import unquote, urlparse
from w2a.core.printer import print_process, print_line


def filter(domain, contents, type, delay=2):
    result_subdomains = []
    result_emails = []

    total = len(contents)
    current = 0

    for i in contents:
        current += 1
        percent = int(current*100/total)
        print_process(percent)

        i['data'] = unquote(i['data'])

        d = domain_filter(domain, unquote(i['url']))
        d += domain_filter(domain, i['data'])

        e = email_filter(domain, i['data'])

        d = sorted(list(set(real_domain(d))))
        e = sorted(list(set(real_email(e))))

        if len(d) >= type or len(e) >= type:
            try:
                data = get_link(i['url'])
                d += domain_filter(domain, data)
                e += email_filter(domain, data)
            except Exception as error:
                pass
            sleep(delay)

        result_subdomains += sorted(list(set(real_domain(d))))
        result_emails += sorted(list(set(real_email(e))))

    print_line('')
    return (result_subdomains, result_emails)


def real_domain(dms):
    res = []
    for d in dms:
        res.append(d.lower().replace('www.', ''))
    return res


def real_email(ems):
    res = []
    for e in ems:
        res.append(e.lower())
    return res


def domain_filter(domain, data):
    domain = domain.replace(".", "\.")
    regex = re.compile('([a-zA-Z0-9]+[a-zA-Z0-9\._-]+' +
                       domain + ')', re.IGNORECASE | re.MULTILINE)
    return regex.findall(data)


def email_filter(domain, data):
    domain = domain.replace(".", "\.")
    regex = re.compile('([a-zA-Z]+[a-zA-Z0-9\._-]+@[a-zA-Z0-9._%+-]*' +
                       domain + ')', re.IGNORECASE | re.MULTILINE)
    return regex.findall(data)


def get_link(url):
    link = "https://docs.google.com/viewer?a=gt&url=" + url
    data = get(link)
    return data

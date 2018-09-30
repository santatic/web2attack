#  modules/harvester.py
#
#  Copyright 2012 VinaKid :">

from w2a.core.templates import Templates
from w2a.lib.searcher import google, bing, yahoo, baidu, exalead, filter
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from w2a.lib.ip import IP
from w2a.lib.file import full_path, read_from_file, append_file

from socket import gethostbyname


class Module(Templates):
    threads = []
    docsthreads = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ############################
        self.version = 1
        self.author = ['VinaKid']
        self.description = 'Get subdomain and email'
        self.detailed_description = 	\
            '\tModule is using to get subdomain and email of domains\n' + \
            ' by bruteforce subdomain or from search engineer\n' +\
            '	$ w2a > set DOMAIN google,bing,yahoo\n' +\
            '	$ w2a > unset DOMAIN\n' +\
            '	$ w2a > set DOMAINLIST [path to domain list])\n' +\
            '- Option TYPE: speed\n' +\
            '- Option SUBLIST: path of subdomain list is using to bruteforce subdomain\n'

        ############################
        self.options.add_string(
            'DOMAIN', 'Target domain (support: domain1,domain2...)', False)
        self.options.add_string('SEARCHER', 'Select search enginee: google, bing, yahoo, baidu, exalead, all',
                                default='google', complete=['google', 'bing', 'yahoo', 'baidu', 'exalead', 'all'])
        self.options.add_integer('LIMIT', 'Set limit search', default=1000)
        self.options.add_string('TYPE', 'Type scan(fast, nomal , slow)',
                                default='slow', complete=['fast', 'nomal', 'slow'])
        self.options.add_integer('DELAY', 'Delay time', default=1)
        self.options.add_boolean(
            'MULTITHREADS', 'Get subdomain and email with multithreading', default=False)
        self.options.add_path('SUBLIST', 'Bruteforce subdomain list',
                              False, default=CONFIG.DATA_PATH + '/dict/subdomain.vn')
        ############################
        self.advanced_options.add_integer(
            'THREADS', 'Thread bruteforce', default=5)
        self.advanced_options.add_boolean(
            'REVERSEIP', 'Reverse ip to find subdomain', False)
        self.advanced_options.add_path(
            'DOMAINLIST', 'Path to domain list', False)
        self.advanced_options.add_path('OUTPUT', 'Output directory', False)

        ############################
        self.ip_helper = IP()

    def run(self, frmwk, args):
        self.frmwk = frmwk
        self.domain = self.options['DOMAIN']
        self.limit = self.options['LIMIT']
        self.searcher = self.options['SEARCHER']
        self.multithread = self.options['MULTITHREADS']
        self.delay = self.options['DELAY']
        self.subbrute = self.options['SUBLIST'] if self.options['SUBLIST'] else [
        ]
        self.domainlist = self.advanced_options['DOMAINLIST']
        self.output = self.advanced_options['OUTPUT']
        self.brutethread = self.advanced_options['THREADS']
        self.reverse_ip = self.advanced_options['REVERSEIP']

        ##################################################
        self.type = 1
        if self.options['TYPE'].strip().lower() == "fast":
            self.type = 2
        elif self.options['TYPE'].strip().lower() == "slow":
            self.type = 0

        ##################################################
        domains = []
        # domain list
        if not self.domain:
            if self.domainlist:
                domains = read_from_file(full_path(self.domainlist))
            else:
                self.frmwk.print_error(
                    'Nothing to do! Must set DOMAIN/DOMAINLIST options first')
                return
        else:
            domains = self.domain.split(',')

        for domain in domains:
            domain = domain.replace('www.', '').strip()
            self.worker(domain)
            if self.output:
                output = full_path(self.output + '/' + domain + '.txt')
                append_file(output, self.emails)

    def worker(self, domain):
        self.subs = [domain]
        self.emails = []
        self.ips = {}

        ##################################################
        subbrute = []
        for ext in ['.', '-', '']:
            for sub in self.subbrute:
                subbrute.append(sub + ext + domain)
        if len(subbrute) > 0:
            self.frmwk.print_status(
                'Starting bruteforce subdomain on thread %d' % self.brutethread)
            self.ips = self.ip_helper.gets(subbrute, self.brutethread)
        del subbrute

        ##################################################
        self.frmwk.print_status("%s : Start search enginee !" % domain)

        keywork = '"@%s" ext:(%s)' % (domain, ' OR '.join(CONFIG.EXTENSION))
        self.frmwk.print_status('Keywork: %s' % keywork)

        searcher = None
        if "google" in self.searcher or self.searcher is "all":
            searcher = google.Google(keywork, self.limit, self.delay)
        if "yahoo" in self.searcher or self.searcher is "all":
            searcher = yahoo.yahoo(keywork, self.limit, self.delay)
        if "bing" in self.searcher or self.searcher is "all":
            searcher = bing.bing(keywork, self.limit, self.delay)
        if "baidu" in self.searcher or self.searcher is "all":
            searcher = baidu.baidu('"@' + domain + '"', self.limit, self.delay)
        if "exalead" in self.searcher or self.searcher is "all":
            searcher = exalead.exalead(keywork, self.limit, self.delay)

        if searcher:
            searcher.start()
            self.threads.append(searcher)

        ##################################################
        for t in self.threads:
            t.join()
            self.frmwk.print_status(
                "Harvesting : <[ {0:<25} {1:d}".format(t.name, len(t.content)))

            if self.multithread:
                ps = Thread(target=filter.filter, args=(
                    domain, t.content, self.type,))
                self.docsthreads.append(ps)
                ps.start()
            else:
                s, e = filter.filter(domain, t.content, self.type)
                self.subs += s
                self.emails += e

        if len(self.docsthreads) > 0:
            for ps in self.docsthreads:
                s, e = ps.join()
                self.subs += s
                self.emails += e

        self.subs.append(domain)
        self.subs = sorted(list(set(self.subs)))
        self.emails = sorted(list(set(self.emails)))

        ############ check subdomain ##############
        self.frmwk.print_status(
            'Checking subdomain in : %d thread' % self.brutethread)
        ips = self.ip_helper.gets(self.subs, self.brutethread)
        for ip in ips.keys():
            if ip in self.ips:
                self.ips[ip] = sorted(list(set(self.ips[ip] + ips[ip])))
            else:
                self.ips[ip] = ips[ip]
        del ips

        ################# reverse ip ###############
        if self.reverse_ip:
            for ip in self.ips.keys():
                rev_ip = self.frmwk.modules['info/reverse_ip']
                rev_ip.options.add_string(
                    'RHOST', 'IP/Domain to reverse(support : ip1,ip2...)', default=ip)
                rev_ip.options.add_boolean(
                    'CHECK', 'check domain is in this IP ', default=True)
                rev_ip.options.add_integer(
                    'THREADS', 'thread check domain', default=10)
                ############################
                rev_ip.advanced_options.add_path(
                    'HOSTLIST', 'Path to domain list', False)
                rev_ip.advanced_options.add_path(
                    'OUTPUT', 'Output directory', False)
                rev_ip.run(self.frmwk, None)
                self.frmwk.reload_module('info/reverse_ip')
                for d in rev_ip.domains:
                    if d.endswith(domain):
                        self.ips[ip].append(d)
                self.ips[ip] = sorted(list(set(self.ips[ip])))

        ###########################################
        self.frmwk.print_line()
        self.frmwk.print_success(
            "Hosts found in search engines:\n------------------------------")
        for ip in self.ips.keys():
            self.frmwk.print_success('IP Server : ' + ip)
            for dm in self.ips[ip]:
                self.frmwk.print_line('\t. ' + dm)
            self.frmwk.print_line()
        self.frmwk.print_line()

        self.frmwk.print_success("Emails found:\n-------------")
        self.frmwk.print_line("\n".join(self.emails))
        self.frmwk.print_line('')

    def close(self):
        self.frmwk.print_status("Closing threads...")

        self.ip_helper.close()
        for t in self.threads:
            if t.isAlive():
                t.terminate()
        for t in self.docsthreads:
            if t.isAlive():
                t.terminate()

from socket import gethostbyname
from w2a.config import CONFIG
from w2a.lib.thread import Thread
from w2a.core.printer import print_process, print_line


class IP():
    threads = []

    def gets(self, domains, thread=1):
        self.ips = {}
        self.domains = domains
        self.sublen = len(domains)
        self.len = 0

        for i in range(thread):
            t = Thread(target=self.get_parallel)
            self.threads.append(t)
            t.start()

        for t in self.threads:
            t.join()

        print_line()
        return self.ips

    def get_parallel(self):
        while len(self.domains) > 0:
            d = self.domains.pop(0)

            self.len += 1
            percent = int(self.len*100/self.sublen)
            print_process(percent)

            try:
                sip = str(gethostbyname(d))
            except:
                try:
                    sip = str(gethostbyname('www.'+d))
                except:
                    continue

            if sip not in CONFIG.IP_WHITE_LIST:
                if sip in self.ips.keys():
                    self.ips[sip].append(d)
                else:
                    self.ips[sip] = [d]

    def close(self):
        for t in self.threads:
            if t.isAlive():
                t.terminate()

import datetime
import commands


class ResolvedIPData(object):
    ip = None
    whois = None
    ptr = None
    datetime = None

    def __init__(self, ip):
        self.ip = ip
        self.ptr = self.reverse_dns()
        self.whois = self.get_whois()
        self.datetime = datetime.datetime.now()

    def reverse_dns(self):
        return '.'.join(reversed(self.ip.split('.'))) + '.in-addr.arpa'

    def get_whois(self):
        return commands.getoutput('whois %s' % self.ip)


class Store(object):
    data_type = ResolvedIPData
    data = []

    __store = None

    def __new__(cls):
        if not cls.__store:
            cls.__store = super(Store, cls).__new__(cls)
        return cls.__store

    def add_object(self, ip):
        obj = self.data_type(ip)
        self.data.append(obj)

    def clear(self):
        self.data = []


store = Store()

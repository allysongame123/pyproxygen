import requests
import threading
import time
import traceback
import random

class ProxyGenerator:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}

    def __init__(self, url, update_interval=300):
        self.url = url
        self.update_interval = update_interval
        self.proxies = []
        self.blacklist = {}
        self.index = 0
        self.event = threading.Event()
        self.lock = threading.Lock()
        self.update_thread = threading.Thread(target=self.updater)
        self.update_thread.start()

    def __next__(self):
        return self.get()

    def get(self):
        while 1:
            with self.lock:
                if not self.proxies:
                    self.event.wait()
                    self.event.clear()

                proxy = self.proxies[self.index]
                self._next()
                if not proxy in self.blacklist:
                    return proxy

    def size(self):
        return len(self.proxies)

    def block(self, proxy):
        with self.lock:
            if not proxy in self.blacklist:
                self.blacklist[proxy] = 1
    
    def unblock(self, proxy):
        with self.lock:
            if proxy in self.blacklist:
                self.blacklist.pop(proxy, None)
    
    def _next(self):
        self.index += 1
        if self.index > len(self.proxies)-1:
            self.index = 0

    def update(self, proxylist):
        random.shuffle(proxylist)
        self.proxies = proxylist
        self.index = min(self.index, len(proxylist)-1)
        self.event.set()
    
    def updater(self):
        while True:
            try:
                with requests.get(self.url,headers=self.headers) as resp:
                    proxylist = resp.text.splitlines()
                    proxylist = list(set(proxylist))
                    self.update(proxylist)
                    del proxylist

            except:
                traceback.print_exc()

            time.sleep(self.update_interval)
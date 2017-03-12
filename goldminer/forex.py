#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Classes specific to http://www.forexpf.ru/ site.

Created on 2016-02-03 11:39

'''
import logging
import time
import re
from bs4 import BeautifulSoup as Soup

from goldminer.scrapper import get_request, create_session, DEFAULT_DELAY
from goldminer.utils import random_seconds

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2017"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

SITE_ROOT = 'http://www.forexpf.ru'

    
class ForexSession(object):
    def __init__(self, proxies=None, delay=DEFAULT_DELAY, on_failure=None):
        self._proxies = proxies
        self._delay = delay
        self._session = None
        self._usd = None # dollar
        self._eur = None # euru
        self._xau = None # gold
        self._xag = None # silver
        self._xpt = None # platinium
        self._xpd = None # palladium
        
        if on_failure is None:
            self._on_failure = self._raise_exception
        else:
            self._on_failure = on_failure
        
        
    def _get_bid(self, table=None, row_offset=1, col_offset=0):
        for i, tr in enumerate(table.find_all('tr')):
            if i == row_offset:
                for j, td in enumerate(tr.find_all('td')):
                    if j == col_offset:
                        m = re.match(r'\d+\.\d+', td.text)
                        logging.debug(td.text)
                        if m:
                            return float(td.text)
                        else:
                            raise AssertionError('Expected decimal, found: <%s>', td.text)
    
    def _get_metal_bid(self, rel_url):
        r = get_request('%s%s' % (SITE_ROOT, rel_url), self.session)
        soup = Soup(r.text, 'lxml')
        table = soup.find('table', class_='stat')
        assert table is not None, 'stat table not found!'
        return self._get_bid(table, 1, 0)


    def get_metal_bids(self):
        self._xau = self._get_metal_bid('/chart/gold/')
        self._xag = self._get_metal_bid('/chart/silver/')
        self._xpt = self._get_metal_bid('/chart/platinum/')
        self._xpd = self._get_metal_bid('/chart/palladium/')

    def get_money_bids(self):
        r = get_request('%s%s' % (SITE_ROOT, '/chart/usdrub/'), self.session)
        soup = Soup(r.text, 'lxml')
        table = soup.find('table', class_='stat')
        assert table is not None, 'USD/EUR table not found!'
        self._usd = self._get_bid(table, 1, 1)
        self._eur = self._get_bid(table, 2, 2)                


    def _raise_exception(self, reason):
        raise RuntimeError(reason)
    
     
    @property
    def session(self):
        '''requests.Session instance, initialized lazily.'''
        if self._session is None:
            self._session = create_session(proxies=self._proxies)
        return self._session
    
     
    @property   
    def usd(self):
        '''US Dollars price in Rubles'''
        return self._usd

    @property   
    def eur(self):
        '''Euro price in Rubles'''
        return self._eur        
        
    @property   
    def xau(self):
        '''Gold price in USD for 1 oz'''
        return self._xau        

    @property   
    def xag(self):
        '''Silver price in USD for 1 oz'''
        return self._xag

    @property   
    def xpt(self):
        '''Platinium price in USD for 1 oz'''
        return self._xpt

    @property   
    def xpd(self):
        '''Palladium price in USD for 1 oz'''
        return self._xpd
    
    def _sleep(self):
        d = self._delay
        s = random_seconds(*d)
        time.sleep(s)
    
        
    def __call__(self, callback=None):
        logging.debug('Starting %s session...', SITE_ROOT)
        try:
            self.get_money_bids()
            self.get_metal_bids()
        except Exception as ex:
            self._on_failure(str(ex))




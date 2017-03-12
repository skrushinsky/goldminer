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
    def __init__(self, proxies=None, delay=DEFAULT_DELAY):
        self._proxies = proxies
        self._delay = delay
        self._session = None
        self._usd = None # dollar
        self._eur = None # euru
        self._xau = None # gold
        self._xag = None # silver
        
        
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


    def get_money_bids(self):
        r = get_request('%s%s' % (SITE_ROOT, '/chart/usdrub/'), self.session)
        soup = Soup(r.text, 'lxml')
        table = soup.find('table', class_='stat')
        assert table is not None, 'USD/EUR table not found!'
        self._usd = self._get_bid(table, 1, 1)
        self._eur = self._get_bid(table, 2, 2)                


    def _on_failure(self, reason):
        logging.error(reason)
    
     
    @property
    def session(self):
        if self._session is None:
            self._session = create_session(proxies=self._proxies)
        return self._session
    
     
    @property   
    def usd(self):
        return self._usd

    @property   
    def eur(self):
        return self._eur        
        
    @property   
    def xau(self):
        return self._xau        

    @property   
    def xag(self):
        return self._xag
    
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




#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The crawler

Created on 2016-02-03 11:39

'''

import logging
import random
import time
import re

from bs4 import BeautifulSoup as Soup
import requests
from requests.exceptions import RequestException

from goldminer.errors import BotDetectedError, EmptyContentError, BadStatusError
from goldminer.utils import random_seconds

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2016"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

ALT_USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:28.0) Gecko/20100101 Firefox/28.0'
    'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0',
    'Mozilla/5.0 (X11; OpenBSD amd64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows NT 6.1; rv:27.3) Gecko/20130101 Firefox/27.3',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-ca) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/531.2+',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; es-ES) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.18.1 (KHTML, like Gecko) Version/5.0 Safari/533.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; ja-JP) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; fr) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; zh-cn) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16'          
]

DEFAULT_TIMEOUT = 15.0
DEFAULT_DELAY = [1.5, 5.0]

DEFAULT_REQUEST_ARGS = {
    'timeout'        : DEFAULT_TIMEOUT,
    'allow_redirects': True, 
}

SITE_ROOT = 'http://www.forexpf.ru'

def pick_user_agent():
    return random.choice(ALT_USER_AGENTS)

def create_session(**kwargs):
    # initialize arguments for requests library
    args = dict(DEFAULT_REQUEST_ARGS)
    args.update(kwargs)
    s = requests.Session()
    headers = args.get('headers', {})
    headers['User-Agent'] = random.choice(ALT_USER_AGENTS)
    s.headers.update(headers)
    
    proxies = kwargs.get('proxies')
    if proxies:
        s.proxies = proxies 
    
    return s



# inspired by https://wiki.python.org/moin/PythonDecoratorLibrary#Retry
def retry_on_exception(tries, delay=5, backoff=2):
    '''
    Retry decorator with expotential backoff.
    
    If decorated function raises BotDetectedError or BadStatusError (the latter
    with resoponse code in range 400- or 500-), it is called again. Any other exception
    is propagated.
    
    Arguments:
    
    tries   : at least 1
    delay   : initial delay in seconds
    backoff : factor by which the delay should lengthen after each failure (>= 1)
    '''
    def decorated(f):
        def f_retry(*args, **kwargs):
            mtries = kwargs.setdefault('tries', tries)
            mdelay = kwargs.setdefault('delay', delay)
            del kwargs['delay']
            del kwargs['tries']
            if tries-mtries  > 0:
                logging.warn('Attempt %d of %d', tries-mtries + 1, tries)
            
            def maybe_retry(ex):
                if mtries > 1:
                    logging.debug('Sleeping for %.1f seconds...', mdelay)
                    time.sleep(mdelay)
                    kwargs['tries'] = mtries - 1
                    kwargs['delay'] = mdelay * backoff
                    f_retry(*args, **kwargs)
                else:
                    raise ex                
            try:
                return f(*args, **kwargs)
            except (BotDetectedError, RequestException, IOError, EmptyContentError) as ex:
                maybe_retry(ex)
            except BadStatusError as ex:
                if ex.response.status_code / 100 in (4, 5):
                    maybe_retry(ex)
                else:
                    raise ex   
            except Exception as ex:
                logging.error('Unhandled exception: %s', ex)
                raise ex                

            
        return f_retry
    return  decorated 
       
def get_once_request(url, session, params=None):
    '''
    Specialized get request
    '''
    # initialize arguments for requests library
    args = dict()
    if params:
        args['params'] = params
    r = session.get(url, **args)
    if r.status_code == 200:
        try:
            r.text
        except AttributeError:
            raise EmptyContentError(url, r)
        else:
            return r

    raise BadStatusError(url, r)                
                
@retry_on_exception(7)
def get_request(url, session, params=None):
    '''
    Specialized get request with 7 retries
    '''
    return get_once_request(url, session, params=params)


def _get_bid(table=None, row_offset=1, col_offset=0):
    for i, tr in enumerate(table.find_all('tr')):
        if i == row_offset:
            for j, td in enumerate(tr.find_all('td')):
                if j == col_offset:
                    m = re.match(r'\d+\.\d+', td.text)
                    logging.debug(td.text)
                    if m:
                        return float(td.text)
                    else:
                        logging.error('Expected decimal, found: <%s>', td.text)


def _get_metal_bid(session, rel_url):
    r = get_request('%s%s' % (SITE_ROOT, rel_url), session)
    soup = Soup(r.text, 'lxml')
    table = soup.find('table', class_='stat')
    if table:
        return _get_bid(table, 1, 0)

def get_gold_bid(session=None, on_success=None, on_failure=None):
    try:
        res = _get_metal_bid(session, '/chart/gold/')
    except Exception as ex:
        on_failure(str(ex))
    else:
        on_success(res)
    

def get_silver_bid(session=None, on_success=None, on_failure=None):
    try:
        res = _get_metal_bid(session, '/chart/silver/')
    except Exception as ex:
        on_failure(str(ex))
    else:
        on_success(res)    


def get_dollar_bid(table=None, on_success=None, on_failure=None):
    try:
        res = _get_bid(table, 1, 1)
    except Exception as ex:
        on_failure(str(ex))
    else:
        on_success(res) 

def get_euro_bid(table=None, on_success=None, on_failure=None):
    try:
        res = _get_bid(table, 2, 2)
    except Exception as ex:
        on_failure(str(ex))
    else:
        on_success(res) 


def get_money_bids_table(session=None, on_success=None, on_failure=None):
    try:
        r = get_request('%s%s' % (SITE_ROOT, '/chart/usdrub/'), session)
        soup = Soup(r.text, 'lxml')
        table = soup.find('table', class_='stat')
    except Exception as ex:
        on_failure(str(ex))
    else:
        if table is None:
            on_failure('USD/EUR table not found')
        else:
            on_success(table) 


            
    
class ForexSession(object):
    def __init__(self, proxies=None, delay=DEFAULT_DELAY):
        self._proxies = proxies
        self._delay = delay
        self._session = None
        self._usd = None
        self._eur = None
        self._xau = None # gold
        self._xag = None # silver
        

    def _on_failure(self, reason):
        logging.error(reason)
    
    def _on_usd(self, val):
        self._usd = val

    def _on_eur(self, val):
        self._eur = val
        
    def _on_usdeur_table(self, table):
        get_dollar_bid(table, self._on_usd, self._on_failure)
        get_euro_bid(table, self._on_eur, self._on_failure)
      
    def _on_xau(self, val):
        self._xau = val        

    def _on_xag(self, val):
        self._xag = val
     
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
        get_money_bids_table(self.session, self._on_usdeur_table, self._on_failure)
        #self._sleep()
        get_gold_bid(self.session, self._on_xau, self._on_failure)
        #self._sleep()
        get_silver_bid(self.session, self._on_xag, self._on_failure)




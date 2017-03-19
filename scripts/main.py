#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Scrapper main script.

Created on 2017-03-11 12:00

'''

import os, sys
from os.path import dirname, abspath
import logging
import argparse
import ConfigParser
from datetime import datetime
import time


__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2017"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

ROOTDIR = abspath(dirname(dirname(__file__)))
sys.path.append(ROOTDIR)
DEFAULT_CONF = os.path.join(ROOTDIR, 'conf', 'local.conf')


from goldminer.forex import ForexSession
from goldminer.utils import str_to_floats, random_seconds
from goldminer.formatters import create_formatter


class ConsoleWriter(object):
    '''
    Writes result to the STDOUT.
    '''
    def __init__(self, formatter=None):
        self._formatter = formatter
        
    def consume(self, **data):
        print self._formatter.format(data)


class Worker(object):
    def __init__(self, once=False, delay=None, proxies=None, consumer=None):
        self._once = once
        self._proxies = proxies
        self._delay = delay
        self._consumer = consumer
    
    def __call__(self):
        while True:
            try:
                forex = ForexSession(proxies=self._proxies)
                forex()
            except Exception as ex:
                logging.error(ex)
            else:
                data = {
                    'usd': forex.usd,
                    'eur': forex.eur,
                    'xau': forex.xau,
                    'xag': forex.xag,
                    'xpt': forex.xpt,
                    'xpd': forex.xpd,
                }
                ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S+00')
                self._consumer.consume(ts=ts, **data)
                logging.debug('Session data saved.')
            finally:
                if self._once:
                    break
                time.sleep(random_seconds(*self._delay))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-c', '--conf', dest='conf', type=str, default=DEFAULT_CONF, help='configuration file')
    parser.add_argument('-l', '--logfile', dest='logfile', type=str, default=None, help='log file')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help='increase output verbosity')
    parser.add_argument('-o', '--once', action='store_true', default=False, help='get one row of data and exit')
    parser.add_argument('-f', '--format', type=str, choices=('json', 'text'), default='text', help='output format')
    args = parser.parse_args()
    
    logging.basicConfig(
        filename=args.logfile,
        level=logging.DEBUG if args.verbose else logging.WARNING,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s', 
    )
    
    if not args.verbose:
        # disable log messages from urllib3 library used by Requests module
        logging.getLogger("urllib3").setLevel(logging.WARNING)        
    
    try:
        config = ConfigParser.ConfigParser()
        config.read(args.conf)
        proxy_addr = config.get('http', 'proxy')
        
        sct = 'format-%s' % args.format
        fmt_args = { k: config.get(sct, k).decode('string_escape') for k in config.options(sct) } \
                   if config.has_section(sct) \
                   else {}
        logging.debug(fmt_args)
        consumer = ConsoleWriter(create_formatter(args.format, fmt_args))
        worker = Worker(
            once=args.once,
            delay=str_to_floats(config.get('http', 'delay')) ,
            proxies = {'http': proxy_addr} if proxy_addr else None,
            consumer = consumer
        )
        worker()

        
    except KeyboardInterrupt:
        logging.info('Interrupted by user')
        sys.exit(1)
    except Exception as ex:
        logging.error(ex, exc_info=args.verbose)
        sys.exit(1)
        
    sys.exit(0)




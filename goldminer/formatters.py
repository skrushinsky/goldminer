#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

'''
Output formatters.

Created on 2017-03-11 17:00

'''

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2017"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

FIELDS = ('ts', 'usd', 'eur', 'xau', 'xag', 'xpt', 'xpd')

class TextFormatter(object):
    '''Converts data to string of columns.
    Default column separator is "|". Change it via 'delimiter' parameter.
    '''
    def __init__(self, delimiter='|'):
        self._delimiter = delimiter
        
    def _format_col(self, k, v):
        if k == 'ts':
            return v
        return '%.3f' % v
        
    def format(self, data):
        '''Given a data dictionary, return a row with columns,
        in order: timestamp, USD, EUR, Gold, Silver, Platinum, Palladium 
        
        Example: 2017-03-12T19:36:30|59.214|63.277|1204.500|17.030|937.000|746.600
        '''
        return self._delimiter.join([ self._format_col(k, data[k]) for k in FIELDS ])
    
    

class JSONFormatter(object):
    '''Converts data to JSON, e.g.:
    {
        "eur": 63.268, 
        "ts": "2017-03-12T19:38:07", 
        "usd": 59.214, 
        "xag": 17.03, 
        "xau": 1204.5, 
        "xpd": 746.6, 
        "xpt": 937.0
    }    
    '''
    def format(self, data):
        '''Given a data dictionary, convert it to JSON.
        '''        
        return json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True).encode('utf8')


FORMATTERS = {
    'text': TextFormatter,
    'json': JSONFormatter,
}


def create_formatter(fmt, options):
    assert fmt in FORMATTERS.keys(), 'Unknown format: %s' % fmt
    return FORMATTERS[fmt](**options)
    
        


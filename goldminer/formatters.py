#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

'''
Output formatters.

Created on 2017-03-11 17:00

'''

class TextFormatter(object):
    '''Converts data to string of columns.
    Default column separator is "|". Change it via 'delimiter' parameter.
    
    Example: 2017-03-11T14:59:50|58.978|62.992|1204.5|17.03
    '''
    def __init__(self, delimiter='|'):
        self._delimiter = delimiter
        
    def _format_col(self, k, v):
        if k == 'ts':
            return v
        return '%.3f' % v
        
    def format(self, data):
        '''Given a data dictionary, return a row with columns,
        in order: timestamp, USD, EUR, XAU, XAG.
        '''
        return self._delimiter.join([ self._format_col(k, data[k]) for k in ('ts', 'usd', 'eur', 'xau', 'xag') ])
    
    

class JSONFormatter(object):
    '''Converts data to JSON, e.g.:
    {
        "eur": 62.992, 
        "ts": "2017-03-11T14:59:50", 
        "usd": 58.978, 
        "xag": 17.03, 
        "xau": 1204.5
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
    
        


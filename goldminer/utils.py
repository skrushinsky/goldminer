#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Utility functions.

Created on 2016-02-03 11:40

'''

import logging
import random
import re

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2016"
__license__ = "Commercial"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"


MIN_SECS = 5
MAX_SECS = 300

def random_seconds(min_seconds=MIN_SECS, max_seconds=MAX_SECS):
    '''sleep for random interval'''
    if min_seconds == max_seconds:
        s = min_seconds
    else:
        s = random.uniform(min_seconds, max_seconds)
        logging.debug("Sleeping for %d sec.", s)
        
    return s   



def str_to_list(s):
    return re.split(r'\s*,\s*', s)

def str_to_floats(s):
    return ( float(d) for d in str_to_list(s) )


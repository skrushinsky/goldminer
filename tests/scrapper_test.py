#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test scrapper utilities.

Created on 2017-03-12 11:28

'''

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2017"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

import sys
from os.path import dirname
sys.path.append(dirname(dirname(__file__)))


import nose
from nose.tools import ok_

from goldminer import scrapper

# import application packages

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2014"
__license__ = "Apache"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"


class TestDefaultSession():
    def __init__(self):
        self.session = scrapper.create_session()
        
    def test_user_agent(self):
        ua = self.session.headers.get('user-agent')
        ok_(ua in scrapper.ALT_USER_AGENTS)




if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s', 
    )    
    nose.runmodule(argv=['-d', '-s', '--verbose'])
            
    
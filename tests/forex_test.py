#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test forex parser.

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

from goldminer import forex

# import application packages

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2014"
__license__ = "Apache"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"



class TestForexSession():
    def __init__(self):
        self.forex = forex.ForexSession()
        self.forex()
    
    def test_usd(self):
        ok_(isinstance(self.forex.usd, list))
    
    def test_eur(self):
        ok_(isinstance(self.forex.eur, list))
        
        
    def test_xau(self):
        ok_(isinstance(self.forex.xau, list))

    def test_xag(self):
        ok_(isinstance(self.forex.xag, list))    
    
    def test_xpt(self):
        ok_(isinstance(self.forex.xpt, list))  

    def test_xpd(self):
        ok_(isinstance(self.forex.xpd, list))  

if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s', 
    )    
    nose.runmodule(argv=['-d', '-s', '--verbose'])
            
    
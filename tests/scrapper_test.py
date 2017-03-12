#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Test scrapper

Created on 2016-02-03 11:55

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
from nose.tools import eq_, ok_, assert_almost_equals

from goldminer import scrapper

# import application packages

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2014"
__license__ = "Apache"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"

session = scrapper.create_session()


def test_dollar_bid():
    def on_value(bid):
        assert isinstance(bid, float)    
    
    def on_table(table):
        scrapper.get_dollar_bid(table, on_value, on_failure)
    
    def on_failure(reason):
        assert False
    
    scrapper.get_money_bids_table(session, on_table, on_failure)
    
def test_euro_bid():
    
    def on_value(bid):
        assert isinstance(bid, float)    
    
    def on_table(table):
        scrapper.get_euro_bid(table, on_value, on_failure)
    
    def on_failure(reason):
        assert False
    
    scrapper.get_money_bids_table(session, on_table, on_failure)




def test_gold_bid():
    def on_success(bid):
        assert isinstance(bid, float)
    
    def on_failure(reason):
        assert False
        
    scrapper.get_gold_bid(session, on_success, on_failure)


def test_silver_bid():
    def on_success(bid):
        assert isinstance(bid, float)
    
    def on_failure(reason):
        assert False
        
    scrapper.get_silver_bid(session, on_success, on_failure)


class TestForexSession():
    def __init__(self):
        self.forex = scrapper.ForexSession()
        self.forex()
    
    def test_usd(self):
        ok_(isinstance(self.forex.usd, float))
    
    def test_eur(self):
        ok_(isinstance(self.forex.eur, float))
        
        
    def test_xau(self):
        ok_(isinstance(self.forex.xau, float))

    def test_xag(self):
        ok_(isinstance(self.forex.xag, float))    
    




if __name__ == '__main__':
    import logging
    logging.basicConfig(
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='%(asctime)s - %(levelname)-8s - %(message)s', 
    )    
    nose.runmodule(argv=['-d', '-s', '--verbose'])
            
    
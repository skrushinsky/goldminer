#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Crawler specific errors.

Created on 2014-07-10 16:06

'''

__author__ = 'Sergey Krushinsky'
__copyright__ = "Copyright 2017"
__license__ = "MIT"
__version__ = "1.0.0"
__email__ = "krushinsky@gmail.com"



class ScrapperError(Exception):
    def __init__(self, url, resp):
        Exception.__init__(self)
        self._url = url
        self._response = resp
    
    @property
    def url(self):
        return self._url
    
    @property
    def response(self):
        return self._response

class BotDetectedError(ScrapperError):
    def __str__(self):
        return 'They caught us!!!'
    
class BadStatusError(ScrapperError):
    def __str__(self):
        return 'Bad status: <%d> at url <%s>' % (self.response.status_code, self.url)   
        

class EmptyContentError(ScrapperError):
    def __str__(self):
        return 'No content at url <%s>' % (self.url) 




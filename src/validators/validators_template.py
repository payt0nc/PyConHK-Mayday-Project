'''
Created on 1 Apr 2017

@author: Comma
'''

from config.config import LogConfig

logger = LogConfig.logger


class Validator(object):
    '''
    classdocs
    '''

    def __init__(self, ticket):
        '''
        Constructor
        '''
        self._ticket = ticket
        self._validation = list()
        self._error_message = list()

    def check(self):
        result = {}
        self.run()
        logger.debug(self._error_message)
        if False in self._validation:
            result['Status'] = False
            result['Info'] = self._error_message
        else:
            result['Status'] = True
            result['Info'] = self._error_message
        return result

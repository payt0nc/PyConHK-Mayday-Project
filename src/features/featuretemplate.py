'''
Created on 1 Apr 2017

@author: Comma
'''
from abc import abstractclassmethod


class Feature(object):
    '''
    classdocs
    '''

    @abstractclassmethod
    def reset(self):
        pass

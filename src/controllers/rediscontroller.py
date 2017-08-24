'''
Created on 3 Apr 2017

@author: Comma
'''
import redis

from config.config import RedisConfig, LogConfig


config = RedisConfig()
logger = LogConfig.logger


class Redis(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        try:
            self.redis = redis.StrictRedis(
                host=config.host, port=config.post, db=config.db)
        except redis.exceptions.ConnectionError as e:
            logger.error(e)

    def insert(self, key, value):
        try:
            result = self.redis.set(key, value)
            logger.info(result)
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def load(self, key):
        try:
            result = self.redis.get(key)
            if result is not None:
                result = result.decode()
            logger.info(result)
            return result
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

    def delete(self, key):
        try:
            logger.debug(key)
            result = self.redis.delete(key)
            logger.debug(result)
            return result
        except redis.exceptions.TimeoutError as timeout:
            logger.error(timeout)
        except redis.exceptions.LockError as locked:
            logger.error(locked)

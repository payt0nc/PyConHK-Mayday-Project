'''
Created on 3 Apr 2017

@author: Comma
'''

from config.config import RedisConfig, LogConfig
import json
import traceback

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



class RedisHelper(Redis):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._post_steps = [
            'Collection', 'Date', 'Price', 'Quantity', 'Status',
            'Section', 'Row', 'Seat', 'Remarks', 'Choice',
            'TelegramInfo'
        ]
        self._search_steps = [
            'Collection', 'Date', 'Price', 'Quantity', 'Status', 'TelegramInfo'
        ]

    @staticmethod
    def get_redis_key(user_id, stage, step):
        key = str(user_id) + '_' + stage + '_' + step
        return key

    def set_cache(self, key, value):
        result = self.insert(key, value)
        return result

    def save_to_redis(self, user_id, stage, step, redisvalue):
        rediskey = self.getRedisKey(user_id, stage, step)
        logger.debug(rediskey)
        self.insert(rediskey, redisvalue)

    def save_telegram_info(self, userinfo, stage):
        logger.debug(userinfo)
        user_id = userinfo.get('id')
        userprofile = json.dumps(userinfo, ensure_ascii=False)
        self.saveToRedis(user_id, stage, 'TelegramInfo', userprofile)

    def load_single_from_redis(self, user_id, stage, step):
        key = self.getRedisKey(user_id, stage, step)
        result = self.load(key)
        return result

    def load_info_from_redis(self, user_id, stage):
        result = self.loadSingleFromRedis(user_id, stage, 'TelegramInfo')
        return result

    def load_ticket_from_redis(self, user_id, stage):
        result = {}
        for step in self._post_steps:
            if step not in ['Choice', 'TelegramInfo']:
                try:
                    rtn = self.load(self.getRedisKey(user_id, stage, step))
                    if step in ['Quantity', 'Section']:
                        result[step] = int(rtn)
                    else:
                        result[step] = rtn
                except:
                    result[step] = None
        return result

    def load_query_from_redis(self, user_id, stage):
        result = {}
        for step in self._post_steps:
            try:
                rtn = self.load(self.getRedisKey(user_id, stage, step))
                if step in ['Quantity', 'Section']:
                    result[step] = int(rtn)
                else:
                    result[step] = rtn
            except:
                result[step] = None
        return result

    def clean_redis(self, user_id, stage):
        try:
            counter = 0
            if stage == 'Post':
                steps = self._post_steps
            if stage == 'Search':
                steps = self._search_steps
            if stage is not None:
                for step in steps:
                    n = self.delete(self.getRedisKey(user_id, stage, step))
                    counter += n
                if counter >= len(steps) - 1:
                    logger.info('User %s cleaned in Redis, Cleaned: %s', user_id, counter)
                    return True
                else:
                    logger.warning('User %s cleaned %s records in Redis. Should be %s',
                                   user_id, counter, len(steps))
                return False
            else:
                for stage in ['Post', 'Search']:
                    steps = self._post_steps + self._search_steps
                    for step in steps:
                        n = self.delete(self.getRedisKey(user_id, stage, step))
                        counter += n
                    if counter >= len(steps) - 1:
                        logger.info('User %s cleaned in Redis, Cleaned: %s', user_id, counter)
                        return True
                    else:
                        logger.warning('User %s cleaned %s records in Redis. Should be %s',
                                       user_id, counter, len(steps))

        except:
            traceback.print_exc()

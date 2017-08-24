'''
Created on 3 Apr 2017

@author: Comma
'''
import json

from config.config import LogConfig
from controllers.rediscontroller import Redis
import traceback


logger = LogConfig.logger


class RedisHelper(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.redis = Redis()
        self._post_steps = [
            'Collection', 'Date', 'Price', 'Quantity', 'Status',
            'Section', 'Row', 'Seat', 'Remarks', 'Choice',
            'TelegramInfo'
        ]
        self._search_steps = [
            'Collection', 'Date', 'Price', 'Quantity', 'Status', 'TelegramInfo'
        ]

    @staticmethod
    def get_redis_key(userid, stage, step):
        key = str(userid) + '_' + stage + '_' + step
        return key

    def set_cache(self, key, value):
        result = self.redis.insert(key, value)
        return result

    def save_to_redis(self, userid, stage, step, redisvalue):
        rediskey = self.get_redis_key(userid, stage, step)
        logger.debug(rediskey)
        self.redis.insert(rediskey, redisvalue)

    def save_telegram_info(self, user_info, stage):
        logger.debug(user_info)
        userid = user_info.get('id')
        userprofile = json.dumps(user_info, ensure_ascii=False)
        self.save_to_redis(userid, stage, 'TelegramInfo', userprofile)

    def load_single_from_redis(self, userid, stage, step):
        key = self.get_redis_key(userid, stage, step)
        result = self.redis.load(key)
        return result

    def load_info_from_redis(self, userid, stage):
        result = self.load_single_from_redis(userid, stage, 'TelegramInfo')
        return result

    def load_ticket_from_redis(self, userid, stage):
        result = {}
        for step in self._post_steps:
            if step not in ['Choice', 'TelegramInfo']:
                try:
                    rtn = self.redis.load(self.get_redis_key(userid, stage, step))
                    if step in ['Quantity', 'Section']:
                        result[step] = int(rtn)
                    else:
                        result[step] = rtn
                except:
                    result[step] = None
        return result

    def load_query_from_redis(self, userid, stage):
        result = {}
        for step in self._post_steps:
            try:
                rtn = self.redis.load(self.get_redis_key(userid, stage, step))
                if step in ['Quantity', 'Section']:
                    result[step] = int(rtn)
                else:
                    result[step] = rtn
            except:
                result[step] = None
        return result

    def clean_all_redis(self, userid, stage):
        try:
            counter = 0
            if stage == 'Post':
                steps = self._post_steps
            if stage == 'Search':
                steps = self._search_steps
            if stage is not None:
                for step in steps:
                    n = self.redis.delete(self.get_redis_key(userid, stage, step))
                    counter += n
                if counter >= len(steps) - 1:
                    logger.info('User %s cleaned in Redis, Cleaned: %s', userid, counter)
                    return True
                else:
                    logger.warning('User %s cleaned %s records in Redis. Should be %s',
                                   userid, counter, len(steps))
                return False
            else:
                for stage in ['Post', 'Search']:
                    steps = self._post_steps + self._search_steps
                    for step in steps:
                        n = self.redis.delete(self.get_redis_key(userid, stage, step))
                        counter += n
                    if counter >= len(steps) - 1:
                        logger.info('User %s cleaned in Redis, Cleaned: %s', userid, counter)
                        return True
                    else:
                        logger.warning('User %s cleaned %s records in Redis. Should be %s',
                                       userid, counter, len(steps))

        except:
            traceback.print_exc()

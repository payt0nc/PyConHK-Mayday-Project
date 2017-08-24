'''
Created on 1 Apr 2017

@author: Comma
'''
import traceback

from telegram.ext import ConversationHandler

from config.config import LogConfig, ContentConfig
from constants import conversations
from constants.replykeyboards import ReplyKeyboards
from constants.stages import Stages
from helpers.requests import RequestHelper
from helpers.redis import RedisHelper

logger = LogConfig().logger

conversations = conversations.MainPanel()
keyboards = ReplyKeyboards()
stage = Stages()
redis = RedisHelper()


def is_in_check_black_list(userid):
    in_black_list = RequestHelper().check_black_list(userid)
    if in_black_list.get('Status'):
        logger.info('%d is in BlackList', userid)
        return True
    else:
        logger.info('%d is NOT in BlackList', userid)
        return False


def is_admin(userid):
    return bool(userid in [113932682])


def start(bot, update):
    try:
        userid = update.message.from_user.id
        username = update.message.from_user.username
        logger.debug(username)
        if is_in_check_black_list(userid):
            update.message.reply_text(conversations.YELLOWCOW)
            return ConversationHandler.END
        else:
            update.message.reply_text(conversations.REMINDER)
            if username == '':
                update.message.reply_text(conversations.USERNAME_MISSING)
                update.message.reply_text(conversations.START % username,
                                          reply_markup=keyboards.actions_keyboard_markup)
            else:
                update.message.reply_text(conversations.START % username,
                                          reply_markup=keyboards.actions_keyboard_markup)
            return stage.MAIN_PANEL
    except:
        traceback.print_exc()


def sos(bot, update):
    update.message.reply_text(conversations.SOS)
    return ConversationHandler.END


def done(bot, update, user_data):
    userid = update.message.from_user.id
    if 'choice' in user_data:
        del user_data['choice']
    redis.clean_all_redis(userid, None)
    try:
        goodbye_path = ContentConfig.cache_path + 'Asin.png'
        with open(goodbye_path, 'rb') as goodbye_pic:
            update.message.reply_photo(goodbye_pic, caption=conversations.DONE)
        goodbye_pic.close()
    except:
        update.message.reply_text(conversations.DONE)
        traceback.print_exc()
    user_data.clear()
    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

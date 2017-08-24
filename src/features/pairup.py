'''
Created on 2 Apr 2017

@author: Comma
'''

import traceback
import json

from telegram import chataction
from telegram.ext.dispatcher import run_async

from config.config import LogConfig
from constants import conversations
from constants.replykeyboards import ReplyKeyboards
from constants.stages import Stages
from features.featuretemplate import Feature
from helpers.redis import RedisHelper
from helpers.requests import RequestHelper


logger = LogConfig.logger
keyboards = ReplyKeyboards()
conversations = conversations.PairUp()
stage = Stages()
requesthelper = RequestHelper()
redishelper = RedisHelper()


class PairUp(Feature):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.tag = 'PairUP'

    def get_seller_profile(self, ticket_id):
        ticket = requesthelper.send_search_ticket_by_ticket_id(ticket_id)
        logger.info(ticket)
        return ticket

    # STEPS:

    @run_async
    def start(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            text = update.message.text
            result = self.get_seller_profile(text)
            if result.get('Status') is True:
                pairup = {
                    "Seller": result.get('Info'),
                    "Buyer": {
                        "first_name": update.message.from_user.first_name,
                        "username": update.message.from_user.username,
                        "last_name": update.message.from_user.last_name,
                        "id": update.message.from_user.id
                    },
                    "MessageToBuyer": ""
                }
                redishelper.save_to_redis(userid, self.tag, 'PairUp',
                                          json.dumps(pairup, ensure_ascii=False))
            else:
                update.message.reply_text(conversations.TYPE_IN_ERROR)
            update.message.reply_text(conversations.REMINDER)
            update.message.reply_text(conversations.START)

        except:
            traceback.print_exc()
        return stage.PAIR_UP_MESSAGE_RECEIVE

    @run_async
    def received_message(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            message = update.message.text
            update.message.reply_text(conversations.MESSAGE % message)
            bot.send_chat_action(
                update.message.chat_id, action=chataction.ChatAction.TYPING)
            pairup = redishelper.load_single_from_redis(
                userid, self.tag, 'PairUp')
            pairup = json.loads(pairup, encoding="UTF-8")
            pairup['MessageToBuyer'] = message
            redishelper.save_to_redis(userid, self.tag, 'PairUp',
                                      json.dumps(pairup, ensure_ascii=False))
            update.message.reply_text(conversations.CONFIRM,
                                      reply_markup=keyboards.pair_up_keyboard_send_message_markup)
        except:
            traceback.print_exc()
        return stage.PAIR_UP_MESSAGE_SEND

    def reset_message(self, bot, update, user_data):
        update.message.reply_text(conversations.RESET)
        return stage.PAIR_UP_MESSAGE_RECEIVE

    def notifly_seller(self, bot, update, user_data):
        userid = update.message.from_user.id
        pairup = json.loads(redishelper.load_single_from_redis(userid, self.tag, 'PairUp'),
                            encoding="UTF-8")
        logger.debug('Seller Profile: %s', pairup.get('Seller'))
        logger.debug('Buyer Profile: %s', pairup.get('Buyer'))
        logger.debug('Message: %s', pairup.get('MessageToBuyer'))

        logger.info('Buyer %s send to Seller %s Message: %s', pairup['Buyer'][
                    'username'], pairup['Seller']['username'], pairup.get('MessageToBuyer'))

        buyer_name = pairup.get('Buyer').get('username')
        seller_id = int(pairup['Seller']['id'])
        message_from = conversations.MSG_FROM + buyer_name

        self.send_message_out(bot, update, seller_id, message_from, pairup)
        update.message.reply_text(conversations.SENT,
                                  reply_markup=keyboards.actions_keyboard_markup)
        return stage.MAIN_PANEL

    @run_async
    def send_message_out(self, bot, update, seller_id, message_from, pairup):
        bot.sendMessage(chat_id=seller_id,
                        text=conversations.NEW_MSG % message_from)
        bot.sendMessage(chat_id=seller_id,
                        text=pairup.get('MessageToBuyer'))

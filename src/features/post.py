'''
Created on 2 Apr 2017

@author: Comma
'''

import traceback
import json

from telegram import ReplyKeyboardMarkup
from telegram.ext.dispatcher import run_async

from config.config import LogConfig
from constants import conversations
from constants.replykeyboards import ReplyKeyboards
from constants.stages import Stages
from features.featuretemplate import Feature
from helpers.redis import RedisHelper
from helpers.requests import RequestHelper
from parsers.ticketparser import TicketParser
from validators.ticketvalidator import TicketValidator


logger = LogConfig.logger
conversations = conversations.PostTickets()
keyboards = ReplyKeyboards()
parser = TicketParser()
redis_helper = RedisHelper()
stage = Stages()


class PostTicket(Feature):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._status = '待交易'
        self.tag = 'Post'

    # STEP:

    @run_async
    def start(self, bot, update, user_data):
        try:
            telegraminfo = {
                "first_name": update.message.from_user.first_name,
                "username": update.message.from_user.username,
                "last_name": update.message.from_user.last_name,
                "id": update.message.from_user.id
            }

            redis_helper.save_telegram_info(telegraminfo, self.tag)
            redis_helper.save_to_redis(update.message.from_user.id, self.tag, 'Status', '待交易')
            update.message.reply_text(
                conversations.START,
                reply_markup=keyboards.post_ticket_keyboard_markup)
            return stage.POST_CONDITION
        except:
            traceback.print_exc()

    @run_async
    def info(self, bot, update, user_data):
        try:
            text = update.message.text
            keyword = conversations.get_keywords(text)
            redis_helper.save_to_redis(update.message.from_user.id, self.tag, 'Choice', keyword)

            if keyword in ['Row', 'Seat', 'Remarks']:
                update.message.reply_text(conversations.INFO % text)
            elif keyword == 'Section':
                update.message.reply_text(conversations.SECTION,
                                          reply_markup=ReplyKeyboardMarkup(
                                              (keyboards.conditiions_keyboard_mapping).get(text))
                                          )
            else:
                update.message.reply_text(conversations.INFO % text,
                                          reply_markup=ReplyKeyboardMarkup(
                                              (keyboards.conditiions_keyboard_mapping).get(text))
                                          )
            return stage.POST_CONDITION_REPLY
        except:
            traceback.print_exc()

    @run_async
    def received(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            text = update.message.text
            choice = redis_helper.load_single_from_redis(userid, self.tag, 'Choice')

            if choice in ['Quantity', 'Section']:
                redis_helper.save_to_redis(userid, self.tag, choice, int(text))
            else:
                redis_helper.save_to_redis(userid, self.tag, choice, text)
            current = redis_helper.load_ticket_from_redis(userid, self.tag)
            logger.debug(current)
            dialog = conversations.RECEVIED_INFO % TicketParser().ticket_tostring(current)
            logger.debug(dialog)
            update.message.reply_text(dialog,
                                      reply_markup=keyboards.post_ticket_keyboard_markup)
        except:
            traceback.print_exc()
            update.message.reply_text(conversations.TYPE_IN_ERROR,
                                      reply_markup=keyboards.post_ticket_keyboard_markup)

        return stage.POST_CONDITION

    @run_async
    def check(self, bot, update, user_data):
        userid = update.message.from_user.id
        ticket = redis_helper.load_ticket_from_redis(userid, self.tag)
        try:
            logger.debug(ticket)
            validation = TicketValidator(ticket).check()

            if validation.get('Status') is True:
                logger.debug(validation.get('Info'))
                update.message.reply_text(conversations.TYPE_IN_CORRECT,
                                          reply_markup=keyboards.post_ticket_keyboard_post_markup)
                return stage.SUBMIT_TICKET
            else:
                logger.debug(validation.get('result'))
                dialog = (conversations.TYPE_IN_WARNING % (
                    validation.get('Info'))).replace('[\'', '').replace('\']', '').replace('\', \'', '\n')
                logger.debug(dialog)
                update.message.reply_text(dialog,
                                          reply_markup=keyboards.post_ticket_keyboard_markup)
                return stage.POST_CONDITION
        except:
            traceback.print_exc()

    @run_async
    def submit(self, bot, update, user_data):
        userid = update.message.from_user.id
        try:
            telegraminfo = json.loads(redis_helper.load_info_from_redis(userid, self.tag),
                                      encoding='UTF-8')
            ticketinfo = redis_helper.load_ticket_from_redis(userid, self.tag)
            ticket = parser.form_ticket(ticketinfo, telegraminfo)
            logger.debug(ticket)
            result = RequestHelper().send_ticket_insert(ticket)
            if result.get('Status'):
                dialog = conversations.INTO_DB % (result.get('Info').get('TicketID'))
            else:
                if result.get('Info') == 'Existed':
                    dialog = conversations.EXISTED
                else:
                    dialog = conversations.ERROR
            update.message.reply_text(dialog,
                                      reply_markup=keyboards.actions_keyboard_markup)
            redis_helper.clean_all_redis(userid, self.tag)
            return stage.MAIN_PANEL
        except:
            traceback.print_exc()

    def reset(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            redis_helper.clean_all_redis(userid, self.tag)
            update.message.reply_text(conversations.RESET,
                                      reply_markup=keyboards.actions_keyboard_markup)
            return stage.MAIN_PANEL
        except:
            traceback.print_exc()

"""
Created on 1 Apr 2017

@author: Comma
"""

import traceback
import time
import json

from telegram import ReplyKeyboardMarkup, chataction
from telegram.ext.dispatcher import run_async

from config.config import LogConfig
from constants import conversations
from constants.stages import Stages
from constants.replykeyboards import ReplyKeyboards
from features.featuretemplate import Feature
from helpers.redis import RedisHelper
from helpers.requests import RequestHelper
from parsers.ticketparser import TicketParser


logger = LogConfig().logger
conversations = conversations.SearchTickets()
keyboards = ReplyKeyboards()
ticketparser = TicketParser()
requesthelper = RequestHelper()
redis_helper = RedisHelper()
stage = Stages()


class Search(Feature):

    def __init__(self):
        self.tag = "Search"

    # STEPS:

    def start(self, bot, update):
        try:
            update.message.reply_text(conversations.START,
                                      reply_markup=keyboards.search_ticket_type_keyboard_markup)
            return stage.CHOOSING
        except:
            traceback.print_exc()

    @run_async
    def condition(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            choice = update.message.text
            logger.info(
                "User: %s ; User Choose: %s", update.message.chat_id, choice)
            logger.debug(conversations.get_ticket_type(choice))
            collection = conversations.get_ticket_type(choice)
            query = {
                "TicketType": collection,
                "TelegramID": userid,
                "Conditions":
                    {
                        "Date": [],
                        "Price": [],
                        "Status": [],
                        "Quantity": []
                    }
            }
            redis_helper.save_to_redis(userid, self.tag, "Query",
                                       json.dumps(query, ensure_ascii=False))
            update.message.reply_text(conversations.CONDITION,
                                      reply_markup=keyboards.ticket_condition_keyboard_markup)
            return stage.TICKET_CONDITION
        except:
            traceback.print_exc()

    @run_async
    def choice(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            text = update.message.text
            logger.info(
                "User: %s ; User Choose: %s", update.message.chat_id, text)
            choice = conversations.get_keywords(text)
            redis_helper.save_to_redis(userid, self.tag, "Choice", choice)
            update.message.reply_text(conversations.CHOICE % text,
                                      reply_markup=ReplyKeyboardMarkup(
                                          (keyboards.conditiions_keyboard_mapping).get(
                                              text)))
            return stage.TICKET_CONDITION_REPLY
        except:
            traceback.print_exc()

    @run_async
    def received_information(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            text = update.message.text
            choice = redis_helper.load_single_from_redis(
                userid, self.tag, "Choice")
            logger.info("User: %s ;User Previous Choice: %s ;User Choose: %s",
                        update.message.chat_id, choice, text)
            query = redis_helper.load_single_from_redis(userid, self.tag, "Query")
            query = json.loads(query, encoding="UTF-8")
            if choice == "Quantity":
                if int(text) not in query['Conditions'][choice]:
                    query['Conditions'][choice].append(int(text))
            else:
                if text not in query['Conditions'][choice]:
                    query['Conditions'][choice].append(text)
            redis_helper.save_to_redis(
                userid, self.tag, 'Query',
                json.dumps(query, ensure_ascii=False))
            updated_query = redis_helper.load_single_from_redis(
                userid, self.tag, "Query")
            updated_condition = json.loads(
                updated_query, encoding="UTF-8").get('Conditions')
            dialog = ticketparser.query_tostring(updated_condition)
            update.message.reply_text(dialog,
                                      reply_markup=keyboards.search_ticket_with_condition_keyboard_markup)
            return stage.TICKET_CONDITION
        except:
            traceback.print_exc()

    @run_async
    def send_query(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            bot.send_chat_action(
                update.message.chat_id, action=chataction.ChatAction.TYPING)
            query = redis_helper.load_single_from_redis(userid, self.tag, "Query")
            query = json.loads(query, encoding="UTF-8")
            result = requesthelper.send_ticket_query(query)
            logger.debug(result)
            if result.get("Status") is True:
                tickets = result.get("Info").get("Tickets")
                logger.debug("User: %s ; Num of Tickets: %s; Tickets: %s",
                             update.message.chat_id, len(tickets), tickets)
                if len(tickets) < 1:
                    dialog = conversations.WITHOUT_TICKETS
                    logger.info("No Ticket Return. Since %s", tickets)
                    update.message.reply_text(dialog,
                                              reply_markup=keyboards.actions_keyboard_markup)
                    return stage.MAIN_PANEL
                elif len(tickets) > 50:
                    update.message.reply_text('搵到的門票太多，無法全部顯示。\n請收窄範圍再搜索',
                                              reply_markup=keyboards.actions_keyboard_markup)
                    return stage.MAIN_PANEL
                else:
                    # logger.debug(tickets)
                    # logger.debug(ticketparser.tickets_tostring(tickets))

                    query_result = {
                        'ticket_ids': ticketparser.trim_ticket_id(tickets),
                        'tickets': tickets
                    }
                    redis_helper.save_to_redis(userid, self.tag, 'search_results',
                                               json.dumps(query_result, ensure_ascii=False))

                    trunck = 5
                    ticket_list = []

                    for i in range(0, len(tickets), trunck):
                        ticket_list.append(tickets[i:i + trunck])

                    logger.info('Ticket_List Len: %d | Total Tickets: %d',
                                len(ticket_list),
                                len(tickets))
                    for ticket_group in ticket_list:
                        dialog = conversations.WITH_TICKETS % ticketparser.tickets_tostring(
                            ticket_group)
                        update.message.reply_text(dialog)
                        logger.debug(ticket_group)
                        bot.send_chat_action(
                            update.message.chat_id,
                            action=chataction.ChatAction.TYPING)
                        time.sleep(1)

                    update.message.reply_text(conversations.AGAIN,
                                              reply_markup=keyboards.search_again_keyboard_markup)
                    return stage.TICKET_CONDITION
            else:
                dialog = conversations.WITHOUT_TICKETS
                update.message.reply_text(dialog,
                                          reply_markup=keyboards.actions_keyboard_markup)
                return stage.MAIN_PANEL
        except:
            traceback.print_exc()

    @run_async
    def pick_ticket(self, bot, update, user_data):
        try:
            userid = update.message.from_user.id
            result = redis_helper.load_single_from_redis(
                userid, self.tag, 'search_results')
            result = json.loads(result, encoding='UTF-8')
            ids = []
            for i in result['ticket_ids']:
                ids.append([i])
            ticket_ids_keyboard = ReplyKeyboardMarkup(
                ids,
                one_time_keyboard=True)
            update.message.reply_text(
                "選擇票據號碼", reply_markup=ticket_ids_keyboard)
            return stage.PAIR_UP_START
        except:
            traceback.print_exc()

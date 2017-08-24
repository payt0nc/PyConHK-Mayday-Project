'''
Created on 2 Apr 2017

@author: Comma
'''
import traceback

from telegram import ReplyKeyboardMarkup, chataction
from telegram.ext.dispatcher import run_async

from config.config import LogConfig
from constants import conversations
from constants.replykeyboards import ReplyKeyboards
from constants.stages import Stages
from features.featuretemplate import Feature
from helpers.requests import RequestHelper
from parsers.ticketparser import TicketParser
from validators.ticketvalidator import TicketValidator


logger = LogConfig.logger
keyboards = ReplyKeyboards()
conversations = conversations.UpdateTicket()
parser = TicketParser()
requesthelper = RequestHelper()
stage = Stages()


class UpdateTickets(Feature):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self, value):
        self._choice = value

    def reset(self):
        self.choice = ''
        logger.debug(self.choice)

    # STEPS:

    @run_async
    def check_my_ticket(self, bot, update, user_data):
        try:
            bot.send_chat_action(update.message.chat_id, action=chataction.ChatAction.TYPING)
            logger.info('UserID : %s', update.message.chat_id)
            search_result = requesthelper.send_search_my_ticket(update.message.chat_id)
            logger.debug(search_result)
            if search_result.get('Status') is True:
                tickets = search_result.get('Info')
                logger.debug(tickets)
                if len(tickets['Sell'] + tickets['Exchange']) < 1:
                    logger.debug('Sell: %s ; Exchange: %s', tickets['Sell'], tickets['Exchange'])
                    update.message.reply_text(conversations.NO_TICKETS,
                                              reply_markup=keyboards.actions_keyboard_markup)
                    return stage.MAIN_PANEL
                else:
                    logger.debug('Sell: %s ; Exchange: %s', tickets['Sell'], tickets['Exchange'])
                    all_tickets = tickets['Sell'] + tickets['Exchange']
                    self.ids = parser.trim_ticket_id(all_tickets)
                    self.tickets_map = parser.tickets_mapping(all_tickets)
                    tickets_keyboard = parser.ids_as_keyboard(self.ids)
                    tickets_list = parser.tickets_tostring(all_tickets)
                    update.message.reply_text(conversations.YOURS % tickets_list,
                                              reply_markup=ReplyKeyboardMarkup(
                                                  tickets_keyboard,
                                                  one_time_keyboard=True))
                    return stage.CHECK_MY_TICKET
            else:
                update.message.reply_text(conversations.NO_TICKETS,
                                          reply_markup=keyboards.actions_keyboard_markup)
                return stage.MAIN_PANEL

        except:
            traceback.print_exc()
            logger.error('Check my Ticket ERROR')
            update.message.reply_text(conversations.NO_TICKETS,
                                      reply_markup=keyboards.actions_keyboard_markup)
            return stage.MAIN_PANEL

    @run_async
    def update_my_ticket(self, bot, update, user_data):
        try:
            ticketid = update.message.text
            logger.debug(ticketid)
            logger.debug(self.ids)
            if ticketid in self.ids:
                self.tobeticket = self.tickets_map.get(ticketid)
                logger.info('To be Update TicketID: %s', ticketid)
                logger.info('To be Update Ticket: %s', self.tobeticket)
                dialog = conversations.START
                update.message.reply_text(dialog,
                                          reply_markup=keyboards.update_ticket_keyboard_post_markup)
                return stage.UPDATE_TICKET
            else:
                dialog = conversations.ERROR
                update.message.reply_text(dialog)
                return stage.CHECK_MY_TICKET
        except:
            traceback.print_exc()

    @run_async
    def update_ticket_info(self, bot, update, user_data):
        text = update.message.text
        logger.debug(text)
        keyword = conversations.get_keywords(text)
        self.choice = keyword
        logger.info('Update item: %s', keyword)
        if keyword in ['Row', 'Seat', 'Remarks']:
            update.message.reply_text(conversations.ITEM % text)
        else:
            update.message.reply_text(conversations.ITEM % text,
                                      reply_markup=ReplyKeyboardMarkup(
                                          (keyboards.conditiions_keyboard_mapping).get(text)))

        return stage.UPDATE_TICKET_REPLY

    @run_async
    def update_ticket_received(self, bot, update, user_data):
        text = update.message.text
        logger.debug(self.tobeticket)
        logger.debug(self.tobeticket.get(self.choice))
        logger.info('User Choise: %s ; Current field: %s ; Update to: %s',
                    self.choice, self.tobeticket.get(self.choice), text)
        try:
            if self.choice in ['Quantity', 'Section']:
                self.tobeticket[self.choice] = int(text)
            else:
                self.tobeticket[self.choice] = text
            logger.info('Updated Ticket Should be: %s', parser.ticket_tostring(self.tobeticket))
            dialog = conversations.INFO % parser.ticket_tostring(self.tobeticket)
            update.message.reply_text(dialog,
                                      reply_markup=keyboards.post_ticket_keyboard_markup)
        except:
            traceback.print_exc()
            update.message.reply_text(conversations.TYPE_IN_ERROR,
                                      reply_markup=keyboards.post_ticket_keyboard_markup)

        return stage.UPDATE_TICKET

    @run_async
    def update_ticket_check(self, bot, update, user_data):
        try:
            logger.debug(self.tobeticket)
            validator = TicketValidator(self.tobeticket)
            self.validation = validator.check()
            logger.info(self.validation)
            if self.validation.get('Status'):
                update.message.reply_text(conversations.TYPE_IN_CORRECT,
                                          reply_markup=keyboards.post_ticket_keyboard_post_markup)
                return stage.UPDATE_TICKET_SUBMIT
            else:
                update.message.reply_text(conversations.TYPE_IN_WARNING % self.validation.get('Info'),
                                          reply_markup=keyboards.post_ticket_keyboard_markup)
                return stage.UPDATE_TICKET
        except:
            traceback.print_exc()

    @run_async
    def submit_ticket(self, bot, update, user_data):
        logger.debug(self.tobeticket)
        telegraminfo = {
            "first_name": update.message.from_user.first_name,
            "username": update.message.from_user.username,
            "last_name": update.message.from_user.last_name,
            "id": update.message.from_user.id
        }
        ticket = parser.form_ticket(self.tobeticket, telegraminfo)
        logger.info('Ticket for sent: %s', ticket)
        result = requesthelper.send_ticket_update(ticket)
        logger.debug(result)
        update.message.reply_text('你張門票已經被紀錄\n',
                                  reply_markup=keyboards.actions_keyboard_markup)
        self.reset()
        return stage.MAIN_PANEL

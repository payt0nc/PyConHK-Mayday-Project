'''
Created on 9 Mar 2017

@author: Comma
'''
from datetime import datetime
import json

from config.config import LogConfig


logger = LogConfig.logger


class TicketFormatter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._ticket = {
            "TicketID": 0,
            "TicketType": "",
            "LastModifyTime": "",
        }
        self._collection_mapping = {
            '原價轉讓': 'Sell',
            '換飛': 'Exchange'
        }

    @staticmethod
    def _get_ticket_message(ticket_id, ticket_info):
        facts = ('\n' +
                 '類別: {Collection}\n' +
                 '門票狀態: {Status}\n' +
                 '票據號碼: {TicketID}\n' +
                 '日期: {Date} \n' +
                 '價錢: {Price}\n' +
                 '數量: {Quantity}\n' +
                 '段數: {Section}\n' +
                 '行數: {Row}\n' +
                 '座位號: {Seat}\n' +
                 '備註: {Remarks}\n').format(
                     TicketID=ticket_id,
                     Collection=ticket_info.get('Collection'),
                     Date=ticket_info.get('Date'),
                     Price=ticket_info.get('Price'),
                     Quantity=ticket_info.get('Quantity'),
                     Status=ticket_info.get('Status'),
                     Section=ticket_info.get('Section'),
                     Row=ticket_info.get('Row'),
                     Seat=ticket_info.get('Seat'),
                     Remarks=ticket_info.get('Remarks')
        )
        return facts

    def form_ticket(self, ticket_info, telegram_info):
        self._ticket['TicketType'] = self._collection_mapping.get(
            ticket_info.get('Collection'))
        self._ticket['TelegramInfo'] = telegram_info
        self._ticket['TicketInfo'] = ticket_info
        self._ticket['TicketID'] = ticket_info.get('TicketID')
        self._ticket['LastModifyTime'] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        return self._ticket

    def query_tostring(self, query):
        facts = (
            '日期: {Date}\n' +
            '價錢: {Price}\n' +
            '數量: {Quantity}\n' +
            '門票狀態: {Status}\n'
        ).format(
            Status=sorted(query.get('Status')),
            Date=sorted(query.get('Date')),
            Price=sorted(query.get('Price')),
            Quantity=sorted(query.get('Quantity')),
        ).replace('[', '').replace(']', '').replace('\'', '')
        return facts

    def tickets_to_string(self, tickets):
        result = ''
        for ticket in tickets:
            if ticket_info.get('Remarks') is None:
                ticket_info['Remarks'] = ''
            if ticket_info.get('TicketID') is None:
                ticket_info['TicketID'] = ''
            result += self._get_ticket_message(
                ticket.get('TicketID'), ticket.get('TicketInfo'))
        if len(tickets) >= 2:
            result  += '====================='
        return result
            

    @staticmethod
    def trim_ticket_id(tickets):
        ticket_ids = []
        for ticket in tickets:
            ticket_ids.append(ticket.get('TicketID'))
        return ticket_ids

    @staticmethod
    def ids_as_keyboard(ticket_ids):
        keyboard = []
        for id in ticket_ids:
            keyboard.append([id])
        keyboard.append(['回主選單'])
        return keyboard

    @staticmethod
    def tickets_mapping(tickets):
        tickets_map = {}
        for ticket in tickets:
            id = ticket.get('TicketID')
            tickets_map[id] = ticket.get("TicketInfo")
            tickets_map[id]['TicketID'] = id
            logger.debug(tickets_map)
        return tickets_map

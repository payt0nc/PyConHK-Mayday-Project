'''
Created on 9 Mar 2017

@author: Comma
'''
from datetime import datetime
from config.config import LogConfig


logger = LogConfig.logger


class TicketParser(object):
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
    def _get_ticket_message(ticketid, ticketinfo):
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
                     TicketID=ticketid,
                     Collection=ticketinfo.get('Collection'),
                     Date=ticketinfo.get('Date'),
                     Price=ticketinfo.get('Price'),
                     Quantity=ticketinfo.get('Quantity'),
                     Status=ticketinfo.get('Status'),
                     Section=ticketinfo.get('Section'),
                     Row=ticketinfo.get('Row'),
                     Seat=ticketinfo.get('Seat'),
                     Remarks=ticketinfo.get('Remarks'))
        return facts

    def form_ticket(self, ticketinfo, telegraminfo):
        self._ticket['TicketType'] = self._collection_mapping.get(
            ticketinfo.get('Collection'))
        self._ticket['TelegramInfo'] = telegraminfo
        self._ticket['TicketInfo'] = ticketinfo
        self._ticket['TicketID'] = ticketinfo.get('TicketID')
        self._ticket['LastModifyTime'] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")
        return self._ticket

    @staticmethod
    def query_tostring(query):
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

    def ticket_tostring(self, ticketinfo):
        if ticketinfo.get('Remarks') is None:
            ticketinfo['Remarks'] = ''
        if ticketinfo.get('TicketID') is None:
            ticketinfo['TicketID'] = ''
        ticket = self._get_ticket_message(
            ticketinfo.get('TicketID'), ticketinfo)
        return ticket

    def tickets_tostring(self, tickets):
        ticket_messages = ''
        for ticket in tickets:
            ticket_messages += self._get_ticket_message(
                ticket.get('TicketID'), ticket.get('TicketInfo'))
        ticket_messages += '====================='
        return ticket_messages

    @staticmethod
    def trim_ticket_id(tickets):
        ticket_ids = []
        for ticket in tickets:
            ticket_ids.append(ticket.get('TicketID'))
        return ticket_ids

    @staticmethod
    def ids_as_keyboard(ticket_ids):
        keyboard = []
        for ticket_id in ticket_ids:
            keyboard.append([ticket_id])
        keyboard.append(['回主選單'])
        return keyboard

    @staticmethod
    def tickets_mapping(tickets):
        tickets_map = {}
        for ticket in tickets:
            ticket_id = ticket.get('TicketID')
            tickets_map[ticket_id] = ticket.get("TicketInfo")
            tickets_map[ticket_id]['TicketID'] = ticket_id
            logger.debug(tickets_map)
        return tickets_map

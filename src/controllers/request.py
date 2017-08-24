'''
Created on 5 Mar 2017

@author: Comma
'''
import requests
import json

from config.config import IrisConfig, LogConfig


logger = LogConfig.logger


class RequestHelper(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.api_url = IrisConfig.url

    def send_ticket_query(self, query_content):
        url = self.api_url + '/searchTicket'
        headers = {'Content-Type': 'application/json'}
        logger.debug(json.dumps(query_content, ensure_ascii=False))
        r = requests.post(
            url, data=json.dumps(query_content, ensure_ascii=False).encode('utf-8'), headers=headers)
        logger.debug(r.__str__())
        return r.json()

    def send_ticket_insert(self, ticket):
        url = self.api_url + '/postTicket'
        headers = {'Content-Type': 'application/json'}
        logger.debug(json.dumps(ticket, ensure_ascii=False))
        r = requests.post(
            url, data=json.dumps(ticket, ensure_ascii=False).encode('utf-8'), headers=headers)
        return r.json()

    def send_ticket_update(self, ticket):
        url = self.api_url + '/updateTicket'
        headers = {'Content-Type': 'application/json'}
        logger.debug(json.dumps(ticket, ensure_ascii=False))
        r = requests.post(
            url, data=json.dumps(ticket, ensure_ascii=False).encode('utf-8'), headers=headers)
        return r.json()

    def send_search_my_ticket(self, userid):
        url = self.api_url + '/myTickets/' + str(userid)
        r = requests.get(url)
        return r.json()

    def send_search_ticket_by_ticket_id(self, ticketid):
        url = self.api_url + '/getTicketByTicketId/' + str(ticketid)
        r = requests.get(url)
        return r.json()

    def check_black_list(self, userid):
        url = self.api_url + '/checkBlackList/' + str(userid)
        r = requests.get(url)
        return r.json()

    def send_promo_metrics(self, userid, event):
        url = self.api_url + '/setPromoHistory?TelegramID={userid}&event={event}'.format_map(
            {'userid': userid, 'event': event})
        requests.get(url)

    def get_userids(self, myid):
        url = self.api_url + '/getUserIDs/' + str(myid)
        r = requests.get(url)
        return r.json()

    def get_admins(self, myid):
        url = self.api_url + '/getAdmins/' + str(myid)
        r = requests.get(url)
        return r.json()

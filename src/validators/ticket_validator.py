'''
Created on Mar 16, 2017

@author: Comma
'''
import string

from Config.Config import TicketValidatorConfig, LogConfig
from Validator.ValidatorTemplate import Validator
import traceback


config = TicketValidatorConfig()
logger = LogConfig.logger


class TicketValidator(Validator):
    '''
    classdocs
    '''

    def check_collection(self):
        try:
            collection = self._ticket.get('Collection')
            if collection is not None:
                if collection in config.collection_values:
                    result = True
                else:
                    self._error_message.append('類別錯誤: %s' % type)
                    result = False
            else:
                self._error_message.append('類別未填喔')
                result = False
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def check_status(self):
        try:
            status = self._ticket.get('Status')
            if status is not None:
                if status in config.status_values:
                    result = True
                else:
                    self._error_message.append('門票狀態錯誤: %s' % status)
                    result = False
            else:
                self._error_message.append('門票狀態未填喔')
                result = False
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def check_date(self):
        try:
            date = self._ticket.get('Date')
            if date is not None:
                if date in config.date_values:
                    result = True
                else:
                    self._error_message.append('日期錯誤: %s' % date)
                    result = False
            else:
                self._error_message.append('日期未填喔')
                result = False
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def check_price(self):
        try:
            price = self._ticket.get('Price')
            if price is not None:
                if price in config.price_values:
                    result = True
                else:
                    self._error_message.append('價錢錯誤: %s' % price)
                    result = False
            else:
                self._error_message.append('價錢未填喔')
                result = False
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def check_quantity(self):
        try:
            quantity = self._ticket.get('Quantity')
            if quantity is not None:
                if type(quantity) is type(int(1)):
                    result = True
                else:
                    self._error_message.append('數量錯誤: %s' % quantity)
                    result = False
            else:
                self._error_message.append('數量未填喔')
                result = False
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def check_section(self):
        try:
            section = self._ticket.get('Section')
            if section is not None:
                if section in range(43, 68):
                    result = True
                else:
                    result = False
                    self._error_message.append('段數錯誤: %s' % section)
            else:
                self._error_message.append('段數未填喔')
                result = False
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    # TODO: Rewise
    def check_row(self):
        try:
            row = self._ticket.get('Row')
            if row is not None:
                if row.isdigit():
                    row = int(row)
                    if row in range(1, 40):
                        result = True
                    else:
                        result = False
                        self._error_message.append('行數錯誤: %s' % row)
                else:
                    row = row.upper()
                    if row in ['AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG',
                               'BA', 'BB', 'BC', 'BD', 'BE', 'BF', 'BG',
                               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                        result = True
                    else:
                        result = False
                        self._error_message.append('行數錯誤: %s' % row)
            else:
                result = False
                self._error_message.append('行數未填喔')
            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def check_seat(self):
        try:
            seats = self._ticket.get('Seat')
            logger.debug(seats)
            if seats is not None:
                if len(seats) > 4:
                    for sperator in [',', '-', '|', ';', '，']:
                        if sperator in seats:
                            seat_list = seats.split(sperator)
                            logger.debug(seat_list)
                    for seat in seat_list:
                        logger.debug(seat)
                        if ' ' in seat:
                            seat = seat.replace(' ', '')
                        logger.debug(seat)
                        try:
                            if int(seat) in range(83, 97):
                                result = True
                            else:
                                result = False
                                self._error_message.append('座位號錯誤: %s' % seat)
                            break
                        except:
                            self._error_message.append('座位號錯誤: %s' % seats)
                            break
                else:
                    if int(seats) in range(83, 97):
                        result = True
                    else:
                        result = False
                        self._error_message.append('座位號錯誤: %s' % seats)
            else:
                result = False
                self._error_message.append('座位號未填喔: %s' % seats)

            self._validation.append(result)
            return result
        except:
            traceback.print_exc()

    def run(self):
        self.check_collection()
        self.check_status()
        self.check_date()
        self.check_price()
        self.check_quantity()
        self.check_section()
        self.check_row()
        self.check_seat()

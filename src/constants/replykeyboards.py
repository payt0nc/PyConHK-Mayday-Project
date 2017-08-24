'''
Created on 5 Mar 2017

@author: Comma
'''
from telegram import ReplyKeyboardMarkup


class ReplyKeyboards(object):
    '''
    classdocs
    '''

    def __init__(self):

        self._actions_keyboard = [
            ['搵門票', '放售門票'],
            ['我的飛', '五迷自發活動'],
            ['完']
        ]

        self._admin_actions_keyboard = [
            ['搵門票', '放售門票'],
            ['我的飛', '五迷自發活動'],
            ['Admin Panel'],
            ['完']
        ]
        self._admin_broadcast_function = [
            ['演唱會Notice'],
            ['任意門應援動作'],
            ['自行輸入信息']
        ]

        self._search_ticket_type = [
            ['原價轉讓', '換飛']
        ]

        self._conditiions_keyboard_mapping = {
            '日期': [
                ['5.10(Wed)', '5.11(Thu)'],
                ['5.13(Sat)', '5.14(Sun)'],
                ['5.16(Tue)', '5.17(Wed)'],
                ['5.19(Fri)', '5.20(Sat)'],
                ['5.22(Mon)', '5.23(Tue)']
            ],

            '價錢': [
                ['$980', '$680', '$380']
            ],

            '數量': [
                ['1', '2'],
                ['3', '4']
            ],

            '門票狀態': [
                ['待交易', '洽談中'],
                ['已交易', '已取消']
            ],

            '段數': [
                ['43', '44', '45', '46', '47'],
                ['48', '49', '50', '51', '52'],
                ['53', '54', '55', '56', '57'],
                ['58', '59', '60', '61', '62'],
                ['63', '64', '65', '66', '67'],
            ],

            '類別': [
                ['原價轉讓', '換飛']
            ]

        }

        self._search_ticket_with_condition_keyboard = [
            ['日期', '價錢'],
            ['數量', '門票狀態'],
            ['重新來過', '搵']
        ]

        self._search_again_keyboard = [
            ['聯絡對方'],
            ['搵多次', '完']
        ]

        self._post_ticket_keyboard = [
            ['類別', '日期', '價錢', '數量'],
            ['段數', '行數', '座位號', '備註'],
            ['重置', '覆核']
        ]

        self._post_ticket_keyboard_post = [['發佈']]

        self._update_ticket_keyboard = [
            ['門票狀態'],
            ['日期', '價錢', '數量'],
            ['段數', '行數', '座位號'],
            ['備註', '覆核']
        ]

        self._ticket_condition_keyboard = [
            ['日期', '價錢', '數量'],
            ['門票狀態', '完']
        ]

        self._pair_up_send_message = [
            ['重寫信息', '送出'],
            ['回主選單']
        ]

        self._support_events = [
            ['523上班餘興節目'],
            ['《五月之約》尋回專屬HOME KONG場的感動']
        ]

    @property
    def actions_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._actions_keyboard, one_time_keyboard=True)

    @property
    def admin_actions_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._admin_actions_keyboard, one_time_keyboard=True)

    @property
    def admin_broadcast_function(self):
        return ReplyKeyboardMarkup(self._admin_broadcast_function, one_time_keyboard=True)

    @property
    def ticket_condition_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._ticket_condition_keyboard, one_time_keyboard=True)

    @property
    def search_ticket_type_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._search_ticket_type, one_time_keyboard=True)

    @property
    def search_ticket_with_condition_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._search_ticket_with_condition_keyboard, one_time_keyboard=True)

    @property
    def search_again_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._search_again_keyboard, one_time_keyboard=True)

    @property
    def support_event_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._support_events, one_time_keyboard=True)

    @property
    def conditiions_keyboard_mapping(self):
        return self._conditiions_keyboard_mapping

    @property
    def post_ticket_keyboard_markup(self):
        return ReplyKeyboardMarkup(self._post_ticket_keyboard, one_time_keyboard=True)

    @property
    def post_ticket_keyboard_post_markup(self):
        return ReplyKeyboardMarkup(self._post_ticket_keyboard_post, one_time_keyboard=True)

    @property
    def update_ticket_keyboard_post_markup(self):
        return ReplyKeyboardMarkup(self._update_ticket_keyboard, one_time_keyboard=True)

    @property
    def pair_up_keyboard_send_message_markup(self):
        return ReplyKeyboardMarkup(self._pair_up_send_message, one_time_keyboard=True)

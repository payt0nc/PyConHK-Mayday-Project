'''
Created on 31 Mar 2017

@author: Comma
'''

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from config.config import TelegramConfig, LogConfig
from constants import conversations
from constants.replykeyboards import ReplyKeyboards
from constants.stages import Stages
from features import mainpanel
from features.pairup import PairUp
from features.post import PostTicket
from features.search import Search
from features.update import UpdateTickets
from features import support

logger = LogConfig().logger
conversations = conversations.MainPanel()
keyboards = ReplyKeyboards()
stage = Stages()
token = TelegramConfig.token


def main():
    updater = Updater(token, workers=64)
    dp = updater.dispatcher

    # Add Feature
    search = Search()
    pairup = PairUp()
    post = PostTicket()
    update = UpdateTickets()

    # Add conversation handler

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', mainpanel.start),
                      CommandHandler('help', mainpanel.sos),
                      CommandHandler('done', mainpanel.done)],
        states={

            stage.MAIN_PANEL: [
                RegexHandler(
                    '^(搵門票)$', search.start),
                RegexHandler(
                    '^(放售門票)$', post.start,
                    pass_user_data=True),
                RegexHandler(
                    '^(我的飛)$', update.check_my_ticket,
                    pass_user_data=True),
                RegexHandler(
                    '^(五迷自發活動)$', support.list_events,
                    pass_user_data=True)
            ],

            stage.CHOOSING: [
                RegexHandler(
                    '^(原價轉讓|換飛)$', search.condition, pass_user_data=True)
            ],

            stage.TICKET_CONDITION: [
                RegexHandler('^(日期|價錢|數量|門票狀態)$',
                             search.choice,
                             pass_user_data=True),
                RegexHandler('^(搵)$', search.send_query, pass_user_data=True),
                RegexHandler('^(搵多次|重新來過)$', mainpanel.start),
                RegexHandler(
                    '^(聯絡對方)$', search.pick_ticket, pass_user_data=True)
            ],

            stage.TICKET_CONDITION_REPLY: [
                MessageHandler(Filters.text,
                               search.received_information,
                               pass_user_data=True)
            ],

            stage.POST_CONDITION: [
                RegexHandler('^(類別|日期|價錢|數量|門票狀態|段數|行數|座位號|備註)$',
                             post.info,
                             pass_user_data=True),
                RegexHandler('^(覆核)$',
                             post.check,
                             pass_user_data=True),
                RegexHandler('^(重置)$',
                             post.reset,
                             pass_user_data=True)
            ],

            stage.POST_CONDITION_REPLY: [
                MessageHandler(Filters.text,
                               post.received,
                               pass_user_data=True)
            ],

            stage.SUBMIT_TICKET: [
                RegexHandler('^(發佈)$',
                             post.submit,
                             pass_user_data=True)
            ],


            stage.CHECK_MY_TICKET: [
                RegexHandler('^(回主選單)$', mainpanel.start),
                MessageHandler(Filters.text,
                               update.update_my_ticket,
                               pass_user_data=True)
            ],

            stage.UPDATE_TICKET: [
                RegexHandler('^(類別|日期|價錢|數量|門票狀態|段數|行數|座位號|備註)$',
                             update.update_ticket_info,
                             pass_user_data=True),
                RegexHandler('^(覆核)$',
                             update.update_ticket_check,
                             pass_user_data=True)
            ],

            stage.UPDATE_TICKET_REPLY: [
                MessageHandler(Filters.text,
                               update.update_ticket_received,
                               pass_user_data=True)],

            stage.UPDATE_TICKET_SUBMIT: [
                RegexHandler('^(發佈)$',
                             update.submit_ticket,
                             pass_user_data=True)
            ],

            stage.PAIR_UP_START: [
                MessageHandler(Filters.text,
                               pairup.start,
                               pass_user_data=True)
            ],

            stage.PAIR_UP_MESSAGE: [
                MessageHandler(Filters.text,
                               pairup.received_message,
                               pass_user_data=True)
            ],

            stage.PAIR_UP_MESSAGE_SEND: [
                RegexHandler('^(重寫信息)$',
                             pairup.reset_message,
                             pass_user_data=True),
                RegexHandler('^(送出)$',
                             pairup.notifly_seller,
                             pass_user_data=True),
                RegexHandler('^(回主選單)$', mainpanel.start, pass_user_data=True)
            ],

            stage.PAIR_UP_MESSAGE_RECEIVE: [
                MessageHandler(Filters.text,
                               pairup.received_message,
                               pass_user_data=True),
            ],

            stage.SUPPORT_EVENT_START: [
                RegexHandler('^(523上班餘興節目)$',
                             support.event_523,
                             pass_user_data=True),
                RegexHandler('^(《五月之約》尋回專屬HOME KONG場的感動)$',
                             support.event_home_kong,
                             pass_user_data=True)
            ]
        },
        fallbacks=[
            RegexHandler(
                '^(Done|done|完)$', mainpanel.done, pass_user_data=True),
            CommandHandler('help', mainpanel.sos),
            CommandHandler('menu', mainpanel.start),
            CommandHandler('done', mainpanel.done, pass_user_data=True),
        ]

    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(mainpanel.error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

'''
stage.ADMIN_CHOICE: [
    RegexHandler('^(演唱會Notice)$',
                    AdminPanel.echo_notice,
                    pass_user_data=True),
    RegexHandler('^(任意門應援動作)$',
                    AdminPanel.echo_dokodemo,
                    pass_user_data=True),
    RegexHandler('^(自行輸入信息)$',
                    AdminPanel.message_input,
                    pass_user_data=True)
],
stage.ADMIN_BOARDCASE_MESSAGE: [
    MessageHandler(Filters.text,
                    AdminPanel.received_message,
                    pass_user_data=True)
],
stage.ADMIN_SEND: [
    RegexHandler('^(重寫信息)$',
                    AdminPanel.reset_message,
                    pass_user_data=True),
    RegexHandler('^(送出)$',
                    AdminPanel.echo_message,
                    pass_user_data=True),
    RegexHandler('^(回主選單)$', mainpanel.start, pass_user_data=True)
]
'''

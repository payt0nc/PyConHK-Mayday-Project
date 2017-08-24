'''
Created on 4 Mar 2017

@author: Comma
'''

import logging.config
import configparser
import os


config = configparser.ConfigParser()
config_path = os.path.dirname(__file__).replace(
    'src/config', 'resources/') + 'config.ini'
config.read(config_path, encoding='UTF-8')

ticket_config_path = os.path.dirname(__file__).replace(
    'src/config', 'resources/') + 'ticket_validation_rules.ini'
ticket_config = configparser.ConfigParser()
ticket_config.read(ticket_config_path, encoding='UTF-8')


class Config(object):
    '''
    classdocs
    '''


class ContentConfig(Config):
    cache_path = os.path.dirname(__file__).replace(
        'src/config', 'resources/cache/')


class LogConfig(Config):
    log_config_path = os.path.dirname(__file__).replace(
        'src/config', 'resources/') + 'log_config.ini'
    logging.config.fileConfig(log_config_path)
    logger = logging.getLogger()


class TelegramConfig(Config):
    token = config.get('telegram', 'token')


class IrisConfig(Config):
    url = config.get('iris', 'url')


class TicketValidatorConfig(Config):
    collection_values = ticket_config.get('Collection', 'values').split('|')
    date_values = ticket_config.get('Date', 'values').split('|')
    section_values = range(43, 68)
    price_values = ticket_config.get('Price', 'values').split('|')
    status_values = ticket_config.get('Status', 'values').split('|')


class RedisConfig(Config):
    host = config.get('redis', 'host')
    post = int(config.get('redis', 'port'))
    db = int(config.get('redis', 'db'))

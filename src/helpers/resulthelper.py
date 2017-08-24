'''
Created on 7 Mar 2017

@author: Comma
'''


def prettify_result(tickets):
    beautyful_result = ''
    beautyful_string_line = ''
    for ticket in tickets:
        for key, value in ticket.items():
            beautyful_string_line += str(key) + ': ' + str(value) + '\n'
        beautyful_result += '\n' + beautyful_string_line
        beautyful_string_line = ''
    return beautyful_result

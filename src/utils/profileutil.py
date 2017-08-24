'''
Created on Jul 22, 2017

@author: Comma
'''


def generate_user_profile(userid, username):
    user_profile = {
        'userId': str(userid),
        'name': str(username)
    }
    return user_profile


def generate_ticket(**kwargv):
    ticket = {
        "category": kwargv.get('category'),
        "status": kwargv.get('status'),
        "event_date": kwargv.get('event_date'),
        "source": kwargv.get('source'),
        "price": kwargv.get('price'),
        "quantity": kwargv.get('quantity'),
        "section": kwargv.get('section'),
        "row": kwargv.get('row'),
        "seat": kwargv.get('seat'),
        "remarks": kwargv.get('remarks'),
        "owner": kwargv.get('owner')
    }
    return ticket


def generate_profile(user=dict(), ticket=dict()):
    profile = {
        'user': user,
        'ticket': ticket
    }
    return profile

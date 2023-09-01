from flask import session

def get_user_id():
    return session.get('user_id')
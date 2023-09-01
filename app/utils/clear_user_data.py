from flask import session

def clear_user_data():
    session.pop('user_id', None)

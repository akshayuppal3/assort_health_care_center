from flask import session

def store_user_id(user_id):
    session['user_id'] = user_id

from functools import wraps
from flask import session
from flask import redirect
from flask import request



def auth_guard(route):
    @wraps(route)
    def wrapper(*args, **kwargs):


        userpages = ['unblock','login','logout','home']
        
        rules = str(request.url_rule).split('/')
        first = rules[1] if rules[1] != '' else 'home'
        
        if 'user_id' in session:
            if not session['is_admin'] and first not in userpages:
                return redirect('/')
        
        elif 'user_id' not in session and 'login' != first:
            return redirect('/login')
            
                
        return route(*args, **kwargs)
    return wrapper
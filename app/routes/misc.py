import datetime
from dateutil.relativedelta import relativedelta
from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import session


from .auth import auth_guard

from classes.utils.types import Response
from classes.core.log import LogOperations
from classes.core.users import UserOperations
from classes.utils.coder import Coder
from classes.utils.validator import Validator

misc_routes = Blueprint('misc', __name__)

@misc_routes.route("/", methods=["GET"])
@auth_guard
def home() -> str:
    is_admin = False
    
    if 'is_admin' in session:
        is_admin = session['is_admin']

    return render_template(
        "main/home.html",
        is_admin=is_admin
        )

@misc_routes.route("/login", methods=["GET","POST"])
@auth_guard
def login() -> str:
    
    if 'user_id' in session:
        return redirect('/')
    
    
    
        
    response = Response(
        error = False,
        data = "Sem erro"
    )
    
    if request.method == "POST":
        
        response = Validator.validate_login(request.form)
        
        if response.error:

            return render_template(
                "main/login.html",
                response = response,
                method=request.method
            )

        user_res = UserOperations.get_by_email(request.form['email'])

        if user_res.error:
            return render_template(
                "main/login.html",
                response = Response(
                        error = True,
                        data = "Esse usuário não existe"
                    ),
                method=request.method
            )
            
        
        user_data = user_res.data
        
        if user_data.password != Coder.hash(request.form['password']):
            return render_template(
                "main/login.html",
                response = Response(
                        error = True,
                        data = "Usuário ou senha incorreta"
                    ),
                method=request.method
            )
        
            
        session['user_id'] = user_data.id
        session['is_admin'] = user_data.permission == 1
        

        return redirect("/")

    return render_template(
        "main/login.html",
        response=response,
        method=request.method
        )

@misc_routes.route("/logout", methods=["GET"])
@auth_guard
def logout():
    session.clear()
    return redirect('/login')

@misc_routes.route("/configuration", methods=["GET"])
@auth_guard
def configuration() -> str:
    
    if 'user_id' in session:
        LogOperations.create({
            "user_id": session['user_id'],
            "page": "/configuration",
            "message": "Acessou pagina de configurações"
        })
            
    # if not session.get('is_admin', False):
    #     return redirect('/')
    
    return render_template("main/configuration.html")

@misc_routes.route("/logs", methods=["GET", "POST"])
@auth_guard
def logs() -> str:
    
    log_list = []
    
    response = LogOperations.list()

    if response.error is False:
        log_list = response.data
    
    # if 'user_id' in session:
    #     LogOperations.create({
    #         "user_id": session['user_id'],
    #         "page": "/logs",
    #         "message": "Acessou pagina de logs"
    #     })
    
    dates = {
        "date_start_str": "0000-00-00",
        "date_end_str": "0000-00-00"
    }
    
    if request.method == 'POST':
        try:
            date_start = datetime.datetime.strptime(request.form['date_start'], "%Y-%m-%d")
        except:
            date_start = datetime.datetime.now()-relativedelta(months=1)
            

        try:
            date_end = datetime.datetime.strptime(request.form['date_end'], "%Y-%m-%d")
        except:
            date_end = datetime.datetime.now()
            
        
        response = LogOperations.list_dated(date_start, date_end)
        if response.error is False:
            log_list = response.data
            
            dates['date_end_str'] = date_end.date().isoformat()
            dates['date_start_str'] = date_start.date().isoformat()
            
            
    return render_template(
        "main/logs.html",
        log_list=log_list,
        response=response,
        date_input=dates,
        method=request.method
        )


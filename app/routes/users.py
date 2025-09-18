from typing import cast

from flask import Blueprint
from flask import render_template
from flask import request
from flask import session


from .auth import auth_guard

from classes.core.log import LogOperations
from classes.utils.types import UserType
from classes.core.users import UserOperations
from classes.utils.types import Response
from classes.utils.coder import Coder
from classes.utils.validator import Validator


users_routes = Blueprint('users', __name__)


@users_routes.route("/users", methods=["GET", "POST"])
@auth_guard
def list_users() -> str:
    
    if 'user_id' in session:
        LogOperations.create({
            "user_id": session['user_id'],
            "page": "/ip-pool",
            "message": "Acessou a página de usuários"
        })
    
    users_list = []
    
    response = UserOperations.list()

    if response.error is False:
        users_list = response.data
        
        
    if request.method == "POST" and "delete" in request.form:
        user_id = request.form["delete"]
        
        response = UserOperations.get(user_id)
        
    
        
        
        if response.error is False:
            user_data = response.data
            response = UserOperations.delete(user_data)

            if 'user_id' in session:
                LogOperations.create({
                    "user_id": session['user_id'],
                    "page": "/ip-pool",
                    "message": f"Removeu usuário {user_data.id} - {user_data.username}"
                })
                
    return render_template(
        "users/list.html",
        user_list=users_list,
        response=response,
        method=request.method
    )

@users_routes.route("/users/create", methods=["GET", "POST"])
@auth_guard
def create_users() -> str:

    user_data:UserType = {
        "id":"",
        "username":"",
        "email":"",
        "password":"",
        "permission":""
    }

    response:Response[str] = Response(
        error = False,
        data = ''
    )
    
    if request.method == 'POST':
        user_data = cast(UserType, dict(**request.form))
        
        user_data["email"] = user_data["email"].strip()
        user_data["password"] = user_data["password"].strip()
        user_data["username"] = user_data["username"].strip()
        
        
        is_valid = Validator.validate_user(user_data)
    
        if is_valid.error:
            return render_template(
                "users/create.html",
                user_data=user_data,
                response=is_valid,
                method=request.method
            )

        user_data['password'] = Coder.hash(user_data['password'])
        
        response = UserOperations.create(user_data)
        
        
        if 'user_id' in session:
            permission = 'Administrador' if user_data['permission'] == '1' else 'Usuário'
            
            LogOperations.create({
                "user_id": session['user_id'],
                "page": "/ip-pool",
                "message": f"Criou usuário {user_data['username']}, Tipo {permission}"
            })

    return render_template(
        "users/create.html",
        user_data=user_data,
        response=response,
        method=request.method
    )

@users_routes.route("/users/<user_id>", methods=["GET", "POST"])
@auth_guard
def edit_users(user_id) -> str:
    
    response = UserOperations.get(user_id)
    
    user = None
    
    user_data:UserType = {
        "id":"",
        "username":"",
        "email":"",
        "password":"",
        "permission":""
    }
    
    if response.error is False:
        user = response.data
        
        user_data = cast(UserType,user.__data__)
    
    if response.error:
        return render_template(
            "users/edit.html",
            user_data=user_data,
            response=response,
            method=request.method
        )
    
    if request.method == "POST":
        
        if response.error is False:
            
            new_user_data = dict(**request.form)
            
            new_user_data["email"] = new_user_data["email"].strip()
            new_user_data["password"] = new_user_data["password"].strip()
            new_user_data["username"] = new_user_data["username"].strip()
            
            is_valid = Validator.validate_user(new_user_data)
    
            if is_valid.error:
                return render_template(
                    "users/edit.html",
                    user_data=user_data,
                    response=is_valid,
                    method=request.method
                )
            
            if user_data['password'] != new_user_data['password']:
                new_user_data['password'] = Coder.hash(new_user_data['password'])
            
            response = UserOperations.update(user, new_user_data)
            permission = 'Administrador' if user_data['permission'] == '1' else 'Usuário'
            if 'user_id' in session:
                LogOperations.create({
                    "user_id": session['user_id'],
                    "page": "/ip-pool",
                    "message": f"Alterou usuário {user_data['id']} - {user_data['username']}, Tipo: {permission}"
                })
                
            user_data = new_user_data
        
    
    return render_template(
        "users/edit.html",
        user_data=user_data,
        response=response,
        method=request.method
    )
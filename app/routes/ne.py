from typing import cast

from flask import Blueprint
from flask import render_template
from flask import request
from flask import session

from .auth import auth_guard

from classes.utils.types import NeType
from classes.core.ne import NeOperations
from classes.core.log import LogOperations
from classes.utils.types import Response
from classes.utils.coder import Coder




ne_routes = Blueprint('ne', __name__)

@ne_routes.route("/ne", methods=["GET", "POST"])
@auth_guard
def list_ne() -> str:

    ne_list = []

    response = NeOperations.list()

    if response.error is False:
        ne_list = response.data

        if 'user_id' in session:
            LogOperations.create({
                "user_id": session['user_id'],
                "page": "/ne",
                "message": "Acessou a página de NEs"
            })

    if request.method == "POST" and "delete" in request.form:
        ne_id = request.form["delete"]

        response = NeOperations.get(ne_id)



        if response.error is False:
            response = NeOperations.delete(response.data)
            
            if 'user_id' in session:
                LogOperations.create({
                    "user_id": session['user_id'],
                    "page": "/ne",
                    "message": f"Removeu NE {response.data.description}"
                })

    
    return render_template(
        "ne/list.html",
        ne_list=ne_list,
        response=response,
        method=request.method
        )

@ne_routes.route("/ne/create", methods=["GET", "POST"])
@auth_guard
def create_ne() -> str:

    ne_data:NeType = {
        "id":"",
        "description": "",
        "host":"",
        "username":"",
        "password":"",
        "poolname":"",
        "vendor":"",
    }

    response:Response[str] = Response(
        error = False,
        data = ''
    )

    if request.method == 'POST':
        ne_data = cast(NeType, dict(**request.form))
        
        ne_data['description'] = ne_data['description'].strip()
        ne_data['host'] = ne_data['host'].strip()
        ne_data['poolname'] = ne_data['poolname'].strip()
        ne_data['username'] = ne_data['username'].strip()
        ne_data['password'] = ne_data['password'].strip()
        
        
        
        ne_data['password'] = str(Coder.encode(ne_data['password'])) 
               
        response = NeOperations.create(ne_data)

        
        if 'user_id' in session:
            LogOperations.create({
                "user_id": session['user_id'],
                "page": "/ne",
                "message": f"Criou NE {ne_data['description']}, Host: {ne_data['host']}, Username: {ne_data['username']}, Vendor: {ne_data['vendor']}"
            })

    return render_template(
        "ne/create.html",
        ne_data=ne_data,
        response=response,
        method=request.method
        )

@ne_routes.route("/ne/<ne_id>", methods=["GET", "POST"])
@auth_guard
def edit_ne(ne_id) -> str:

    ne_data:NeType = {
        "id":"",
        "description": "",
        "host":"",
        "username":"",
        "password":"",
        "vendor":"",
    }
    
    response = NeOperations.get(ne_id)


    if response.error is False:
        ne = response.data
        
        ne_data = cast(NeType,ne.__data__)
    
    if request.method == "POST":
        
        if response.error is False:
            new_ne_data = cast(NeType, dict(**request.form))
            
            new_ne_data['description'] = new_ne_data['description'].strip()
            new_ne_data['host'] = new_ne_data['host'].strip()
            new_ne_data['poolname'] = new_ne_data['poolname'].strip()
            new_ne_data['username'] = new_ne_data['username'].strip()
            new_ne_data['password'] = new_ne_data['password'].strip()
            
            
            
            if new_ne_data['password'] != ne_data['password']:
                new_ne_data['password'] = str(Coder.encode(new_ne_data['password'])) 

            
            response = NeOperations.update(ne, new_ne_data)

            if 'user_id' in session:
                LogOperations.create({
                    "user_id": session['user_id'],
                    "page": "/ne",
                    "message": f"Editou NE {ne_data['id']} {request.form['description']}, Host: {request.form['host']}, Username: {request.form['username']}, Vendor: {request.form['vendor']}"
                })
    
    return render_template(
        "ne/edit.html",
        ne_data=ne_data,
        response=response,
        method=request.method
        )
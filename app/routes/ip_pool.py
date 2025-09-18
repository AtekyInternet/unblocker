from typing import cast

from flask import Blueprint
from flask import render_template
from flask import request
from flask import session


from .auth import auth_guard

from classes.utils.types import IpPoolType
from classes.core.ip_pool import IpPoolOperations
from classes.core.log import LogOperations
from classes.utils.types import Response
from classes.utils.validator import Validator


ip_pool_routes = Blueprint('ip_pool', __name__)

@ip_pool_routes.route("/ip-pool", methods=["GET", "POST"])
@auth_guard
def list_ip_pool() -> str:


    ip_pool_list = []

    response = IpPoolOperations.list()

    if response.error is False:
        ip_pool_list = response.data

    if 'user_id' in session:
        LogOperations.create({
            "user_id": session['user_id'],
            "page": "/ip-pool",
            "message": "Acessou a página de Pools de IP"
        })

    if request.method == "POST" and "delete" in request.form:
        pool_id = request.form["delete"]

        response = IpPoolOperations.get(pool_id)



        if response.error is False:
            ip_pool = response.data
            response = IpPoolOperations.delete(response.data)
            if 'user_id' in session:
                LogOperations.create({
                    "user_id": session['user_id'],
                    "page": "/ip-pool",
                    "message": f"Removeu Pool de IP {ip_pool.id} - {ip_pool.description}, Faixa: {ip_pool.pool}"
                })


    return render_template(
        "ip-pool/list.html",
        ip_pool_list=ip_pool_list,
        response=response,
        method=request.method
    )

@ip_pool_routes.route("/ip-pool/create", methods=["GET", "POST"])
@auth_guard
def create_ip_pool() -> str:
    ip_pool:IpPoolType = {
        "id":"",
        "pool":"",
        "description":""
    }

    response:Response[str] = Response(
        error = False,
        data = ''
    )

    if request.method == 'POST':
        
        ip_pool = cast(IpPoolType, dict(**request.form))
        
        ip_pool["description"] = ip_pool['description'].strip()
        ip_pool["pool"] = ip_pool["pool"].strip()
        
        
        is_valid = Validator.validate_pool(ip_pool)
        
        if is_valid.error:
            return  render_template(
                "ip-pool/create.html",
                pool_data=ip_pool,
                response=is_valid,
                method=request.method
            )        
        
        
        response = IpPoolOperations.create(ip_pool)
        
        if 'user_id' in session:
            LogOperations.create({
                "user_id": session['user_id'],
                "page": "/ip-pool",
                "message": f"Criou Pool de IP {ip_pool['description']}, Faixa: {ip_pool['pool']}"
            })

    return  render_template(
        "ip-pool/create.html",
        pool_data=ip_pool,
        response=response,
        method=request.method
        )


@ip_pool_routes.route("/ip-pool/<pool_id>", methods=["GET", "POST"])
@auth_guard
def edit_ip_pool(pool_id) -> str:
    
    ip_pool_data:IpPoolType = {
        "id":"",
        "pool":"",
        "description":""
    }
    
    response = IpPoolOperations.get(pool_id)


    if response.error is False:
        ip_pool = response.data
        
        ip_pool_data = cast(IpPoolType,ip_pool.__data__)
    
    if request.method == "POST":
        
        
        if response.error is False:
            
            new_pool = dict(**request.form)
            
            new_pool["description"] = new_pool['description'].strip()
            new_pool["pool"] = new_pool["pool"].strip()
            
            is_valid = Validator.validate_pool(new_pool)
        
            if is_valid.error:
                return  render_template(
                    "ip-pool/edit.html",
                    pool_data=ip_pool_data,
                    response=is_valid,
                    method=request.method
                )
            
            
            response = IpPoolOperations.update(ip_pool, new_pool)

            if 'user_id' in session:
                LogOperations.create({
                    "user_id": session['user_id'],
                    "page": "/ip-pool",
                    "message": f"Editou Pool de IP {ip_pool.id} - {new_pool['description']}, Faixa: {new_pool['pool']}"
                })

    return render_template(
        "ip-pool/edit.html",
        pool_data=ip_pool_data,
        response=response,
        method=request.method
        )
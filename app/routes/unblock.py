from typing import List
from typing import Dict

import ipaddress

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request
from flask import session


from .auth import auth_guard

from classes.core.ip_pool import IpPoolOperations
from classes.utils.types import IpPoolType
from classes.utils.types import Response
from classes.core.bulk import BulkOperations
from classes.utils.ixc import IXC 

unblock_routes = Blueprint('unblock', __name__)

@unblock_routes.route("/unblock", methods=["GET", "POST"])
@auth_guard
def unblock_search() -> str:
    response = Response(
        error = True,
        data = "Por favor informe um contrato valido"
    )
    
    if request.method == 'POST' and 'contract' in request.form:
        
        if request.form['contract'] == "" or int(request.form['contract'], 10) < 1:
            return render_template(
                "unblock/search.html",
                response=response,
                method=request.method
            )
        
        login_res = IXC.listLogin(request.form['contract'])
        
        if login_res.error:
            
            return render_template(
                "unblock/search.html",
                response=login_res,
                method=request.method
            )

        ip_pools_res = IpPoolOperations.list()
        
        
        if ip_pools_res.error:
            return render_template(
                "unblock/search.html",
                response=ip_pools_res,
                method=request.method
            )
        
        ip_pools = [ ipaddress.ip_network(pool['pool']) for pool in ip_pools_res.data ]
        
        
        logins = login_res.data

        is_valid = []
        
        for login in logins:
            for pool in ip_pools:
                if ipaddress.IPv4Address(login['ip']) in pool:
                    is_valid.append(login)
                    break
        
        if len(is_valid) > 1:
            return redirect(f"/unblock/{request.form['contract']}")
        
        
        login_id = is_valid[0]['id']
        return  redirect(f"/unblock/{request.form['contract']}/{login_id}")

    return render_template("unblock/search.html")

@unblock_routes.route("/unblock/<contract>", methods=["GET"])
@auth_guard
def unblock_list(contract) -> str:
    
    login_list_res = IXC.listLogin(contract)
    
    if login_list_res.error:
        
        return render_template(
            "unblock/search.html",
            response=login_list_res,
            method=request.method
        )
    
    
    
    ip_pools_res = IpPoolOperations.list() 
    
    if ip_pools_res.error:
        return render_template(
            "unblock/search.html",
            response=ip_pools_res,
            method=request.method
        )

    
    ip_pools = [ ipaddress.ip_network(pool['pool']) for pool in ip_pools_res.data ]
    
    
    logins = login_list_res.data

    is_valid = []
    
    for login in logins:
        for pool in ip_pools:
            if ipaddress.IPv4Address(login['ip']) in pool:
                is_valid.append(login)
                break
    
    if len(is_valid) > 1:
        return render_template(
            "unblock/list.html",
            login_list=login_list_res.data,
            contract=contract
        )
    

    login_id = is_valid[0]['id']
    return  redirect(f"/unblock/{contract}/{login_id}")


@unblock_routes.route("/unblock/<contract>/<login_id>", methods=["GET","POST"])
@auth_guard
def unblock_config(contract, login_id) -> str:
    
    login = session.get('login')
    
    if login is None:
        print('em teoria não é para essa função ser chamada mais de uma vez')
        
        logins_res = IXC.listLogin(contract)

        login = None

        if logins_res.error:
            
            return render_template(
                "unblock/search.html",
                response=logins_res,
                method=request.method
            )

        logins = logins_res.data
        
        ip_pools_res = IpPoolOperations.list() 
        
        if ip_pools_res.error:
            return render_template(
                "unblock/search.html",
                response=ip_pools_res,
                method=request.method
            )


        ip_pools = [ ipaddress.ip_network(pool['pool']) for pool in ip_pools_res.data ]

        is_valid = []

        for login in logins:
            for pool in ip_pools:
                if ipaddress.IPv4Address(login['ip']) in pool:
                    is_valid.append(login)
                    break

        for item in is_valid:
            if str(item['id']) == login_id:
                login = item
                break

            
        session['login'] = login
        
    if login is None:
        not_found_login = Response(
            error = True,
            data = "Login não encontrado"
        )
        return render_template(
            "unblock/search.html",
            response=not_found_login,
            method=request.method
        )



    if request.method == 'POST':
        if request.form['action'] == 'block':
            BulkOperations.remove(login['razao'], login['ip'])
        
        elif request.form['action'] == 'unblock':
            BulkOperations.add(login['razao'], login['ip'])
            
    result = BulkOperations.check(login['ip'])
    

    
    return render_template(
        "unblock/config.html",
        response = result,
        customer = login
    )

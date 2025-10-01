from typing import List
from typing import Dict
from typing import Union
from typing import cast

from classes.vendors.base import VendorBase
from classes.utils.ssh import ShellSSh

from classes.utils.types import Response

class Huawei(VendorBase):
    
    def __init__(self, host:str, username:str, password:str, port:str = '9922'):
        self.host:str = host
        self.username:str = username
        self.password:str = password
        self.port:str = port

        self.credentials:Dict[str, str | int] = {
            "host": host,
            "username": username,
            "password": password,
            "port": int(port, 10)
        }

    def list(self, pool:str) -> Union[Response[str], Response[List[Dict[str,str]]]]:

        result:str
        try:
            with ShellSSh(**self.credentials) as ssh:

                ssh.send('screen-length 512 temporary')

                ssh.send('system-view')

                ssh.send(f'acl ip-pool {pool}')
                result = ssh.send('display this')
                

        except Exception as err:
            return Response(
                error = True,
                data = 'Erro ao listar IPs - ' + str(err)
            )

        lines:List[str] = result.splitlines()[3:-2]

        ip_list:List[Dict[str,str]] = []
        for line in lines:
            config:List[str] = line.rsplit(' ', 2)
            if len(config) > 1:
                ip_list.append({
                    "id": "",
                    "address": config[1]
                })

        return Response(
            error = False,
            data  = ip_list
        )

    def get(self, pool:str, ip_address:str) -> Union[Response[str], Response[Dict[str,str]]]:

        ip_list:Union[Response[str],Response[List[Dict[str,str]]]] = self.list(pool)
        
        if ip_list.error and isinstance(ip_list.data, str):
            return cast(Response[str], ip_list)

        if isinstance(ip_list.data, list):
            for ip in ip_list.data:
                if 'address' in ip.keys() and \
                    ip_address == ip.get('address',''):
                    return Response(
                        error = False,
                        data = ip
                    )

        return Response(
            error = True,
            data = "Ip não encontrado"
        )

    def add(self, pool:str, ip_address:str, name:str) -> Response[str]:
        response:Response[str] = Response(
            error = False,
            data = 'Ip cadastrado com sucesso'
        )

        ip_found:Response[str] | Response[Dict[str,str]] = self.get(pool, ip_address)

        if not ip_found.error and isinstance(ip_found.data, str):
            return response


        try:
            with ShellSSh(**self.credentials) as ssh:

                ssh.send('system-view')

                ssh.send(f'acl ip-pool {pool}')
                result = ssh.send(f'ip address {ip_address} 0.0.0.0')


                lines:List[str] = result.splitlines()

                if len(lines) > 0 and lines[-1].startswith('Error:'):
                    response.error = True
                    response.data = "Erro ao adicionar regra"

                if response.error is False:
                    ssh.send('commit')
                    ssh.send('run save')
                    ssh.send('y')

        except Exception as err:
            return Response(
                error = True,
                data = 'Erro ao adicionar IP - ' + str(err)
            )

        return response

    def remove(self, pool:str, ip_address:str) -> Response[str]:

        response:Response[str] = Response(
            error = False,
            data = 'Removido com sucesso'
        )

        result:Response[str] | Response[Dict[str,str]] = self.get(pool, ip_address)

        if response.error and isinstance(result.data, str):
            return Response(
                error = False,
                data = "Ip não encontrado"
            )

        try:
            with ShellSSh(**self.credentials) as ssh:

                ssh.send('system-view')

                ssh.send(f'acl ip-pool {pool}')

                received = ssh.send(f'undo ip address {ip_address} 0.0.0.0')

                lines:List[str] = received.splitlines()
                
                if len(lines) > 0 and lines[-1].startswith('Error:'):
                    response.error = True
                    response.data = "Erro ao adicionar regra"

                if response.error is False:

                    ssh.send('commit')
                    ssh.send('run save')
                    ssh.send('y')



        except Exception as err:
            return Response(
                error = True,
                data = 'Erro ao remover IP - ' + str(err)
            )


        return response

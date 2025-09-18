from typing import List
from typing import Dict
from typing import Union
from typing import cast

from classes.vendors.base import VendorBase

from librouteros import connect
from librouteros import Api
from librouteros.api import Path

from classes.utils.types import Response


class Mikrotik(VendorBase):

    DEFAULT_RESOURCE = "/ip/firewall/address-list"

    def __init__(self, host:str, username:str, password:str, port:str = '8728'):

        self.host:str = host
        self.username:str = username
        self.password:str = password
        self.port:str = port

        self.credentials = {
            "host": host,
            "username": username,
            "password": password,
            "port": port
        }

    def list(self, pool:str) -> Union[Response[str], Response[List[Dict[str,str]]]]:

        ip_list:List[Dict[str,str]] = []

        try:
            router:Api = connect(**self.credentials)

            response:Path  = router.path(Mikrotik.DEFAULT_RESOURCE)

            port_list = list(response)

            for item in port_list:
                if item.get('list','') == pool and item.get('address') is not None:
                    ip_list.append({
                        "id": item['.id'],
                        "address": item['address']
                    })

            router.close()

        except Exception as err:
            return Response(
                error = True,
                data = 'Erro ao listar IP - ' + str(err)
            )

        return Response(
            error = False,
            data = ip_list
        )

    def get(self, pool:str, ip_address:str)  -> Union[Response[str], Response[Dict[str,str]]]:
        ip_list:Response[str] | Response[List[Dict[str,str]]] = self.list(pool)

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
        item:Dict[str, str] = {
            "list": pool,
            "address": ip_address,
            "comment": name
        }

        try:
            router:Api = connect(**self.credentials)

            path:Path  = router.path(Mikrotik.DEFAULT_RESOURCE)

            path.add(**item)

            router.close()

        except Exception as err:
            return Response(
                error = True,
                data = 'Erro ao adicionar IP - ' + str(err)
            )

        return Response(
            error = False,
            data = 'Ip cadastrado com sucesso'
        )

    def remove(self, pool:str, ip_address:str) -> Response[str]:

        response:Response[str] = Response(
            error = False,
            data = 'Removido com sucesso'
        )

        result:Union[Response[str], Response[Dict[str,str]]] = self.get(pool, ip_address)

        if result.error:
            return Response(
                error = False,
                data = "Ip não encontrado"
            )

        try:
            router:Api = connect(**self.credentials)

            path:Path  = router.path(Mikrotik.DEFAULT_RESOURCE)

            if isinstance(result.data, dict) and 'id' in result.data.keys():
                path.remove(result.data['id'])

            router.close()

        except Exception as err:
            return Response(
                error = True,
                data = 'Erro ao remover IP - ' + str(err)
            )

        return response

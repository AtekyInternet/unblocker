"""
    Essa classe define as operações em massa
"""

from typing import List
from typing import cast
import asyncio

from classes.utils.types import NeType
from classes.utils.types import Response
from classes.utils.text import Text
from classes.utils.coder import Coder



from classes.vendors import vendor_classes
from classes.vendors.base import VendorBase
from .ne import NeOperations

class AsyncBulk:
    @staticmethod
    async def ne_adder(ne:NeType, customer:str, ip_address:str) -> Response[str]:
        vendor = vendor_classes[ne['vendor']]
        router:VendorBase = vendor(ne['host'], ne['username'], Coder.decode(ne['password']))
        
        result = await asyncio.to_thread(router.add, ne['poolname'], ip_address, customer)
        return result
    
    @staticmethod
    async def ne_remover(ne:NeType, ip_address:str) -> Response[str]:
        vendor = vendor_classes[ne['vendor']]
        router:VendorBase = vendor(ne['host'], ne['username'], Coder.decode(ne['password']))
        
        result = await asyncio.to_thread(router.remove, ne['poolname'], ip_address)
        return result
    
    @staticmethod
    async def ne_checks(ne:NeType, ip_address:str) -> Response[str]:
        vendor = vendor_classes[ne['vendor']]
        router:VendorBase = vendor(ne['host'], ne['username'], Coder.decode(ne['password']))
        
        result = await asyncio.to_thread(router.get, ne['poolname'], ip_address)
        return result
    
    @staticmethod
    async def adder(ne_list:List[NeType], customer:str, ip_address:str)  -> List[Response[str]]:
        tasks = [AsyncBulk.ne_adder(ne, customer, ip_address) for ne in ne_list]
        result = await asyncio.gather(*tasks)
        return result
    
    @staticmethod
    async def remover(ne_list:List[NeType], ip_address:str)  -> List[Response[str]]:
        tasks = [AsyncBulk.ne_remover(ne, ip_address) for ne in ne_list]
        result = await asyncio.gather(*tasks)
        return result

    @staticmethod
    async def checker(ne_list:List[NeType], ip_address:str)  -> List[Response[str]]:
        tasks = [AsyncBulk.ne_checks(ne, ip_address) for ne in ne_list]
        result = await asyncio.gather(*tasks)
        return result
    
    
class BulkOperations:
    
    @staticmethod
    def add(customer:str, ip_address:str) -> Response[str]:
    
        response = NeOperations.list()
        
        if response.error:
            return cast(Response[str], response)
        
        nes:List[NeType] = response.data
        
        result_list = asyncio.run(AsyncBulk.adder(nes, Text.normalize(customer) ,ip_address))
        
        errors = [result for result in result_list if result.error]
        
        if len(errors) > 0:
            return Response(
                error = True,
                data = "Erro ao remover bloqueio dos roteadores"
            )
        
        return Response(
            error = False,
            data = "IP liberado com sucesso"
        )
        
    @staticmethod
    def remove(customer:str, ip_address:str) -> Response[str]:
    
        response = NeOperations.list()
        
        if response.error:
            return cast(Response[str], response)
        
        nes:List[NeType] = response.data
        
        result_list = asyncio.run(AsyncBulk.remover(nes, ip_address))
        
        errors = [result for result in result_list if result.error]
        
        if len(errors) > 0:
            return Response(
                error = True,
                data = "Erro ao incluir bloqueio nos roteadores"
            )
        
        return Response(
            error = False,
            data = "IP removido com sucesso"
        )
        
    @staticmethod
    def check(ip_address:str) -> Response[str]:
    
        response = NeOperations.list()
        
        if response.error:
            return cast(Response[str], response)
        
        nes:List[NeType] = response.data

        quantity:int = len(nes)
        
        configured:int = 0
        
        result_list = asyncio.run(AsyncBulk.checker(nes, ip_address))
        
        for result in result_list:
            if not result.error:
                configured+=1

            
        if configured == quantity:
            return Response(
            error = True,
            data = "liberado"
        )
        
        return Response(
            error = False,
            data = "bloqueado"
        )
        
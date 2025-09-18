from typing import Dict

from peewee import DataError
from peewee import DatabaseError
from peewee import IntegrityError
from peewee import OperationalError
from peewee import ProgrammingError
from peewee import DoesNotExist

from classes.utils.types import Response
from classes.db import IpPool
from classes.db import mysql_db

class IpPoolOperations:
    @staticmethod
    def list():
        response = Response(
            error = True,
            data = "Não foi possível coletar as pool de IPs do banco de dados"
        )
        ip_pool_list = []
        
        try:
            with mysql_db.atomic():
                ip_pool_list = IpPool.select().dicts()
            response.data = list(ip_pool_list)
            response.error = False
            
            return response
        
        except DoesNotExist:
            response.data = "Nenhum pool de IP foi encontrado no banco de dados"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de pool IP inválida"
            
        except DatabaseError:
            response.data = "Não foi possivel listar as pools de IP"
        
        return response
    

    @staticmethod
    def get(pool_id):
        response = Response(
            error = True,
            data = "Não foi possível coletar as pool de IP"
        )
    
        try:
            pool = IpPool.get_or_none(id=pool_id)
            
            if pool is not None:
                response.error = False
                response.data = pool
                return response

            return response
            
            
        except DoesNotExist:
            response.data = "Pool de IP não existe"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de pool IP inválida"
        
        except DatabaseError:
            response.data = "Não foi possivel encontrar pool de IP"
        
        return response
    
    @staticmethod
    def update(pool:IpPool, new_data:Dict[str, str ]):
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível alterar pool de IP"
        )
        
        try:
            
            with mysql_db.atomic():
                pool.__data__.update(new_data)
                pool.save()
            
        
            response = Response(
                error = False,
                data = "Pool de IP atualizado com sucesso"
            )
            
        
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except DoesNotExist:
            response.data = "Pool de IP não existe"
            
        except DataError:
            response.data = "Dados incompativeis com o banco de dados"
        
        except IntegrityError:
            response.data = "Dados incompativeis com as restrições"
            
        return response
    
    def delete(pool:IpPool):
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível remover pool de IP"
        )
        
        try:
        
            with mysql_db.atomic():
                pool.delete_instance()

            response.data = "Pool de IP removido com sucesso"
            response.error = False
        
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"
        
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except DoesNotExist:
            response.data = "Esse pool de IP não existe"
        
        return response
    
    def create(data):
        
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível adicionar pool de IP"
        )
        
        try:
            with mysql_db.atomic():
                
                by_pool = IpPool.get_or_none(pool=data['pool'])
                by_description = IpPool.get_or_none(description=data['description'])
                
                if by_pool is None and by_description is None:
                    IpPool.create(**data)
                
                    response.data = "Pool de IP criado com sucesso"
                    response.error = False
                    
                else:
                    response.data = 'Não foi possível criar pool de IP. Essa pool de IP já existe'
                
                
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"

        except DataError:
            response.data = "Dados incompativeis com o banco de dados"

        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
            
        return response
        
        
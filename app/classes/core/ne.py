from typing import Dict
from typing import Union
from typing import List


from peewee import DataError
from peewee import DatabaseError
from peewee import IntegrityError
from peewee import OperationalError
from peewee import ProgrammingError
from peewee import DoesNotExist

from classes.utils.types import Response
from classes.db import Ne
from classes.db import mysql_db

class NeOperations:
    @staticmethod
    def list():
        response = Response(
            error = True,
            data = "Não foi possível coletar os NEs do banco de dados"
        )
        ne_list = []
        
        try:
            with mysql_db.atomic():
                ne_list = list(Ne.select().dicts())

            response.data = ne_list
            response.error = False
            
            return response
        
        except DoesNotExist:
            response.data = "Nenhum NE foi encontrado no banco de dados"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de NE inválida"
            
        except DatabaseError:
            response.data = "Não foi possivel listar as NEs"
        
        return response
    

    @staticmethod
    def get(ne_id):
        response = Response(
            error = True,
            data = "Não foi possível coletar Nes"
        )
    
        try:
            ne = Ne.get_or_none(id=ne_id)
            
            if ne is not None:
                response.error = False
                response.data = ne
                return response

            return response
            
        except DoesNotExist:
            response.data = "NE não existe"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de NE inválida"
        
        except DatabaseError:
            response.data = "Não foi possivel encontrar NE"
        
        return response
    
    @staticmethod
    def update(ne:Ne, new_data:Dict[str, str ]):
        response:Union[Response[str], Response[Dict[str, str ]]] = Response(
            error = True,
            data = "Não foi possível alterar NE"
        )
        
        try:
            
            
            with mysql_db.atomic():
                ne.__data__.update(new_data)
                ne.save()
            
        
            response = Response(
                error = False,
                data = "NE atualizado com sucesso"
            )
            
        
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except DoesNotExist:
            response.data = "NE não existe"
            
        except DataError:
            response.data = "Dados incompativeis com o banco de dados"
        
        except IntegrityError:
            response.data = "Dados incompativeis com as restrições"
            
        return response
    
    def delete(ne:Ne):
        response:Union[Response[str], Response[Dict[str, str ]]] = Response(
            error = True,
            data = "Não foi possível remover NE"
        )
        
        try:
        
            with mysql_db.atomic():
                ne.delete_instance()

            response.data = "NE removido com sucesso"
            response.error = False
        
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"
        
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except DoesNotExist:
            response.data = "Esse NE não existe"
        
        return response
    
    def create(data):
        
        response:Union[Response[str]] = Response(
            error = True,
            data = "Não foi possível adicionar NE"
        )
        
        try:
            with mysql_db.atomic():
                
                by_name = Ne.get_or_none(description=data['description'])
                by_host = Ne.get_or_none(host=data['host'])
                
                if by_name is None and by_host is None:
                    Ne.create(**data)
                
                    response.data = "NE criado com sucesso"
                    response.error = False
                    
                else:
                    response.data = 'Não foi possível criar NE. Essa NE já existe'
                
                
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"

        except DataError:
            response.data = "Dados incompativeis com o banco de dados"

        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
            
        return response
        
        
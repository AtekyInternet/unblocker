from datetime import timezone, timedelta


from peewee import DataError
from peewee import IntegrityError
from peewee import OperationalError
from peewee import ProgrammingError
from peewee import DoesNotExist
from peewee import DatabaseError

from classes.utils.types import Response
from classes.db import Log
from classes.db import User
from classes.db import mysql_db

gmt_minus_3 = timezone(timedelta(hours=-3))

class LogOperations:
    def create(data):
        
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível adicionar pool de IP"
        )
        
        try:
            with mysql_db.atomic():
                
                Log.create(**data)
            
                response.data = "Log criado com sucesso"
                response.error = False
                
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"

        except DataError:
            response.data = "Dados incompativeis com o banco de dados"

        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
            
        return response
        
    @staticmethod
    def list():
        response = Response(
            error = True,
            data = "Não foi possível coletar os logs do banco de dados"
        )
        log_list = []
        
        try:
            with mysql_db.atomic():
                log_list = Log.select(Log, User.username)\
                        .join(User, on=(Log.user_id == User.id))\
                        .order_by(Log.datetime.desc())\
                        .dicts()
                for log in log_list:
                    log["datetime"] = log["datetime"].astimezone(gmt_minus_3)

            response.data = log_list
            response.error = False
            
            return response
        
        except DoesNotExist:
            response.data = "Nenhum log foi encontrado no banco de dados"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de log inválida"
            
        except DatabaseError:
            response.data = "Não foi possivel listar as logs"
        
        return response
    
    def list_dated(start,end):
        response = Response(
            error = True,
            data = "Não foi possível coletar os logs do banco de dados"
        )
        log_list = []
        
        try:
            with mysql_db.atomic():
                log_list = Log.select(Log, User.username)\
                        .join(User, on=(Log.user_id == User.id))\
                        .where(Log.datetime.between(start, end))\
                        .order_by(Log.datetime.desc())\
                        .dicts()
                
                for log in log_list:
                    log["datetime"] = log["datetime"].astimezone(gmt_minus_3)

            response.data = log_list
            response.error = False
            
            return response
        
        except DoesNotExist:
            response.data = "Nenhum log foi encontrado no banco de dados"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de log inválida"
            
        except DatabaseError:
            response.data = "Não foi possivel listar as logs"
        
        return response
    
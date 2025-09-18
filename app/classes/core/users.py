from typing import Dict


from peewee import DataError
from peewee import DatabaseError
from peewee import IntegrityError
from peewee import OperationalError
from peewee import ProgrammingError
from peewee import DoesNotExist

from classes.utils.types import Response
from classes.db import User
from classes.db import mysql_db

class UserOperations:
    @staticmethod
    def list():
        response = Response(
            error = True,
            data = "Não foi possível coletar os usuários do banco de dados"
        )
        users_list = []
        
        try:
            with mysql_db.atomic():
                users_list = User.select().where(User.active==True).dicts()

            response.data = users_list
            response.error = False
            
            return response
        
        except DoesNotExist:
            response.data = "Nenhum usuário foi encontrado no banco de dados"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de usuários inválida"
            
        except DatabaseError:
            response.data = "Não foi possivel listar os usuários"
        
        return response
    

    @staticmethod
    def get(user_id):
        response = Response(
            error = True,
            data = "Não foi possível coletar usuário"
        )

        try: 
            user = User.get_or_none(id=user_id)
            
            if user is not None:
                response.error = False
                response.data = user
                return response

            return response
            
        except DoesNotExist:
            response.data = "Usuário não existe"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de usuários inválida"
        
        except DatabaseError:
            response.data = "Não foi possivel encontrar usuário"
        
        return response
    
    @staticmethod
    def get_by_email(email):
        response = Response(
            error = True,
            data = "Não foi possível coletar usuário"
        )
    
        try: 
            user = User.get(email=email, active=True)
            
            response.error = False
            response.data = user
            
        except DoesNotExist:
            response.data = "Usuário não existe"
            
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except ProgrammingError:
            response.data = "Tabela ou coluna de usuários inválida"
        
        except DatabaseError:
            response.data = "Não foi possivel encontrar usuário"
        
        return response
    
    @staticmethod
    def update(user:User, new_data:Dict[str, str ]):
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível alterar usuário"
        )
        
        try:
            
                    
            with mysql_db:
                user.__data__.update(new_data)
                user.save()
            
            response = Response(
                error = False,
                data = "Usuário atualizado com sucesso"
            )
            
        
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except DoesNotExist:
            response.data = "Usuário não existe"
            
        except DataError:
            response.data = "Dados incompativeis com o banco de dados"
        
        except IntegrityError:
            response.data = "Dados incompativeis com as restrições"
            
        return response
    
    def delete(user:User):
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível remover usuário"
        )
        
        try:
            """
            Tecnicamente não exclui, só marca como inativo pra não aparecer mais e nem logar    
            """
            with mysql_db:
                user.active=False;
                user.save()

            response.data = "Usuário removido com sucesso"
            response.error = False
        
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"
        
        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
        
        except DoesNotExist:
            response.data = "Esse usuário não existe"
        
        return response
    
    def create(data):
        
        response:Response[str] = Response(
            error = True,
            data = "Não foi possível adicionar usuário"
        )
        
        try:
            with mysql_db:
                
                by_email = User.get_or_none(email=data['email'])
                by_username = User.get_or_none(username=data['username'])
                
                
                if by_email is None and by_username is None:
                    User.create(**data)
                
                    response.data = "Usuário criado com sucesso"
                    response.error = False
                    
                else:
                    response.data = 'Não foi possível criar usuário. Esse usuário já existe'
                
                
        except IntegrityError:
            response.data = "Dados sendo usados por outra tabela"

        except DataError:
            response.data = "Dados incompativeis com o banco de dados"

        except OperationalError:
            response.data = "Problema na conexão ou permissões insuficientes no banco de dados"
            
        return response
        
        
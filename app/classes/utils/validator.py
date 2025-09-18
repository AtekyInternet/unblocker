import re
import ipaddress
from .types import Response
from .types import UserType
from .types import NeType
from .types import IpPoolType


class Validator:

    EMAIL_PATTERN = r"^\S+@\S+\.\S+$";

    @staticmethod
    def validate_user(form:UserType) -> Response[str]:


        # Verifica nome
        if len(form['username']) < 3 or len(re.findall('[^\w\s]', form['username'])) > 0:
            return Response(
                error = True,
                data = "Nome de usuário possui caracteres inválidos"
            )

        # Verifica email
        if not re.search(Validator.EMAIL_PATTERN, form['email']):
            return Response(
                error = True,
                data = "Email inválido"
            )

        # Verifica senha
        if len(form['password']) < 6:
            return Response(
                error = True,
                data = "Senha muito curta"
            )

        # verifica permissão
        if form['permission'] not in ('0', '1'):
            return Response(
                error = True,
                data = "Permissão inválida"
            )

        return Response(
            error = False,
            data = "Usuário válido"
        )


    @staticmethod
    def validate_login(form:UserType) -> Response[str]:
        
        # Verifica email
        if not re.search(Validator.EMAIL_PATTERN, form['email']):
            return Response(
                error=True,
                data="Email inválido"
            )


        # Verifica senha
        if len(form['password']) < 6:
            return Response(
                error = True,
                data = "Senha inválida"
            )


        return Response(
            error = False,
            data = ""
        )
    
    @staticmethod
    def validate_ne(form:NeType) -> Response[str]:
        
        if len(form['description']) < 4:
            return Response(
                error = True,
                data = "Nome muito curto"
            )
            
        if len(form['poolname']) < 4:
            return Response(
                error = True,
                data = "Insira um nome de pool valido"
            )
            
        if len(form['username']) < 4:
            return Response(
                error = True,
                data = "Insira um usuário valido"
            )
            
        if len(form['password']) < 4:
            return Response(
                error = True,
                data = "Insira uma senha valida"
            )
        
        try: 
            ipaddress.IPv4Address(form['host'])
            return Response(
                error = False,
                data = ""
            )
        except:
            return Response(
                error = True,
                data = "Insira um host válido"
            )
            
    @staticmethod
    def validate_pool(form:IpPoolType) -> Response[str]:
        
        if len(form['description']) < 4:
            return Response(
                error = True,
                data = "Nome muito curto"
            )

        
        try: 
            ipaddress.ip_network(form['pool'], strict=False)
            return Response(
                error = False,
                data = ""
            )
        except:
            return Response(
                error = True,
                data = "Insira uma pool válida"
            )
        
                
    
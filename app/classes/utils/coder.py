"""
Esse modulo define uma classe utilitaria
para codificação, decodificação e hashing de strings

Classes definidas:
    - Coder

"""
import os, hashlib
from cryptography.fernet import Fernet

class Coder:
    """
    Essa classe possui algumas utilidades 
    para codificação, decodificação e hashing de strings
    """
    KEY = str(os.getenv('UNBLOCK_CRYPT_KEY')).encode('ascii')
    TOKER = Fernet(KEY)
    
    @staticmethod
    def decode(value:str) -> str:
        """
        Decodifica a string
        usando a chave pre-configurada na .env

        Args:
            value (str): String codificada

        Returns:
            str: String decodificada
        """
        decrypted = Coder.TOKER.decrypt(value)
        return decrypted.decode('utf-8')

    @staticmethod
    def encode(value:str) -> str:
        """
        Codifica a string
        usando a chave pre-configurada na .env

        Args:
            value (str): A string original

        Returns:
            str: A string codificada
        """
        encoded = value.encode('utf-8')
        result = Coder.TOKER.encrypt(encoded)
        return result.decode('utf-8')

    @staticmethod
    def hash(value:str) -> str:
        """
        Transforma string em hash
        

        Args:
            value (str): String original

        Returns:
            str: Hash criada
        """
        ho = hashlib.sha256(value.encode('utf-8'))
        return ho.hexdigest()

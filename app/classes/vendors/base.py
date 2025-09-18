from abc import ABC, abstractmethod
from typing import List
from typing import Dict
from typing import Union


from classes.utils.types import Response

class VendorBase(ABC):
    @abstractmethod
    def __init__(self, host:str, username:str, password:str, port:str): ...
    
    @abstractmethod
    def list(self, pool:str) -> Union[Response[str], Response[List[Dict[str,str]]]]: ...
    
    @abstractmethod
    def get(self, pool:str, ip_address:str) -> Union[Response[str], Response[Dict[str,str]]]:...
    
    @abstractmethod
    def add(self, pool:str, ip_address:str, name:str) -> Response[str]: ...
    
    @abstractmethod
    def remove(self, pool:str, ip_address:str) -> Response[str]:...
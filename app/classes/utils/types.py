from dataclasses import dataclass
from typing import TypeVar
from typing import Generic
from typing import TypedDict

T = TypeVar("T")

@dataclass
class Response(Generic[T]):
    """
    Type for generic function return
    
    This class takes a single type argument.
    That is the type of message data
    
    Type Vars:
        T: The type of the response message payload
    
    Attributes:
        error (bool): If theres a error Its set to True, If not False
        data (T): Message text or data returned 
    """
    error: bool
    data: T | str

class UserType(TypedDict):
    id: str
    username: str
    email: str
    password: str
    permission: str
    
class IpPoolType(TypedDict):
    id: str
    description: str
    pool: str

class NeType(TypedDict):
    id: str
    description: str
    host: str
    username: str
    password: str
    poolname: str
    vendor: str
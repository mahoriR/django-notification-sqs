import abc, typing
from ..errors import Error

class RequestABC(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def from_request(cls, request_data)->(typing.Any, Error.ErrorInfo):...

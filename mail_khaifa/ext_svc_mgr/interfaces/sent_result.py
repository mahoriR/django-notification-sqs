import abc

class SentResult(abc.ABC):
    '''
    Implemented by result of external service(SMS/Email) API call's result representation
    '''
    @abc.abstractmethod
    def is_success(self):...

    @abc.abstractmethod
    def get_external_id(self):...

    @abc.abstractmethod
    def get_failure_reason(self):...

import abc

class QueueableABC(abc.ABC):
    '''
        Interface (Technically ABC) implemented by All Queuable entities
    '''
    @abc.abstractmethod
    def to_dict(self):
        '''
        To be used for Queueing
        '''
        ...

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dict_data):
        '''
        To recreate from Queued Data
        '''
        ...

    @abc.abstractmethod
    def get_max_timestamp(self)->int:
        '''
         Enqueing will fail if current timestamp is past this. 0 means ignore.
        '''
        ...


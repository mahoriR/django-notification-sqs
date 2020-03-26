import abc

class QueueableABC(abc.ABC):
    '''
        Interface (Technically ABC) implemented by All Queuable entities
    '''
    @abc.abstractmethod
    def to_json(self):
        '''
        To be used for Queueing
        '''
        ...

    @abc.abstractmethod
    def from_json(self):
        '''
        To recreate from Queued Data
        '''
        ...

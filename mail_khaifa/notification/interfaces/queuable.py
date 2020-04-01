import abc, typing

class QueueableABC(abc.ABC):
    '''
    Interface (Technically ABC) implemented by All Queuable entities
    '''


    @abc.abstractmethod
    def to_dict(self)->typing.Dict:...
    # TBD: Raise bug on coverage. If ... are after the comment (we want doctstring to be present)
    # in that case it is getting marked as not covered in coverage.
    '''
    To be used for Queueing
    '''

    @classmethod
    @abc.abstractmethod
    def from_dict(cls, dict_data:typing.Dict):...
    '''
    To recreate from Queued Data
    '''

    @abc.abstractmethod
    def get_max_timestamp(self)->int:...
    '''
    Enqueing will fail if current timestamp is past this. 0 means ignore.
    '''


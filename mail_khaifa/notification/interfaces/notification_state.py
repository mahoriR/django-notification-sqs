import abc, collections

CallBackInfo=collections.namedtuple('CallBackInfo', ('required','cb_url'))

class NotificationStateABC(abc.ABC):

    '''
    Class for Notification State.

        1. Used to update DB with new state
        2. To Callback services for state transition

    Data from External Services for state transition is converted to this class before 

        1. Executing callback
        2. Or Queueing to CB queue if (1) fails
    '''

    @abc.abstractmethod
    def get_notification_state(self):
        ...

    @abc.abstractmethod
    def get_notifiaction_id(self):...

    @abc.abstractmethod
    def get_callback_info(self)->CallBackInfo:
        '''
        Return NamedTuple ('Callback Required', 'CB URL')
        '''
        ...

    @abc.abstractmethod
    def get_notification_type(self):...

    @abc.abstractmethod
    def get_retry_count(self):
        '''
        How many times already tried calling the CB URL
        '''
        ...
    @abc.abstractmethod
    def __init__(self, n_state, n_id, cb_url, cb_states, retry_count=0):
        ...

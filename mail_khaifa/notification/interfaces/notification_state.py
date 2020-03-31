import abc, collections

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
    def get_notifiaction_cb_url(self)->str:...

    @abc.abstractmethod
    def set_retry_count(self, retry_count:int):...

    @abc.abstractmethod
    def get_retry_count(self):
        '''
        How many times already tried calling the CB URL
        '''
        return 0

    @abc.abstractmethod
    def get_max_retry_count(self):
        return 3

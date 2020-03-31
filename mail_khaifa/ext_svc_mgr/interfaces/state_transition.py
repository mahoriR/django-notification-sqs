import abc

from ...notification.models import Notification

class StateTransitionABC(abc.ABC):
    '''
    State transition for a notification
    '''

    @abc.abstractmethod
    def get_external_id(self)->str:...

    @abc.abstractmethod
    def get_updated_state(self)->Notification.NotificationType:...

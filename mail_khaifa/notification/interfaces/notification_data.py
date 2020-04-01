import abc, enum, uuid
from typing import List, Dict

class NotificationDataABC(abc.ABC):
    '''
    Interface implemented by all Notification Data
    '''
    class PriorityType(enum.IntEnum):
        HIGH = 3
        MEDIUM = 2
        LOW = 1

    @abc.abstractmethod
    def get_priority(self)->PriorityType:...

    @abc.abstractmethod
    def get_notifiaction_id(self)->uuid.UUID:...

    @abc.abstractmethod
    def get_notification_type(self)->int:...

    @abc.abstractmethod
    def get_payload(self)->Dict:...

    @abc.abstractmethod
    def get_notification_cb_url(self)->str:...

    @abc.abstractmethod
    def get_notification_cb_states(self)->List[int]:...

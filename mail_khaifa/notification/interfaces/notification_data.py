import abc, enum, uuid
from typing import List

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
    def get_entity_ids(self)->List:...

    @abc.abstractmethod
    def get_addressing_group_ids(self):...

    @abc.abstractmethod
    def get_addressing_type(self)->AddressingType:...

    @abc.abstractmethod
    def get_notification_type(self)->int:...

    @abc.abstractclassmethod
    def get_notification_content(self):
        '''
        Get Content as per the notificaiton type
        '''
        ...
    @abc.abstractmethod
    def notification_cb_url(self)->str:
        ...
    @abc.abstractmethod
    def notification_cb_states(self)->List[int]:
        ...


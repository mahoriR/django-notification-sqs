import abc

class NotificationDataABC(abc.ABC):
    '''
    Interface implemented by all Notification Data
    '''

    class AddressingType(object):
        __slots__=[]
        ENTITY = 'entity'
        ENTITY_GROUP = 'entity_grp'

    class PriorityType(object):
        __slots__=[]
        HIGH = 3
        MEDIUM = 2
        LOW = 1

    @abc.abstractmethod
    def get_priority(self):...

    @abc.abstractmethod
    def get_notifiaction_id(self):...

    @abc.abstractmethod
    def get_entity_ids(self):...

    @abc.abstractmethod
    def get_addressing_group_ids(self):...

    @abc.abstractmethod
    def get_addressing_type(self):...

    @abc.abstractmethod
    def get_notification_type(self):...

    @abc.abstractclassmethod
    def get_notification_content(self):
        '''
        Get Content as per the notificaiton type
        '''
        ...
    @abc.abstractmethod
    def notification_cb_url(self):
        ...
    @abc.abstractmethod
    def notification_cb_states(self):
        ...


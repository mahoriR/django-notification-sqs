from .notification_data import NotificationDataABC
from .queuable import QueueableABC

class QueuableNotificationDataABC(NotificationDataABC, QueueableABC): pass
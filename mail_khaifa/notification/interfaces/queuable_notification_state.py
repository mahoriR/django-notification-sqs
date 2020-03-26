from .queuable import QueueableABC
from .notification_state import NotificationStateABC

class QueuableNotificationStateABC(NotificationStateABC, QueueableABC):pass
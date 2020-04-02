from django.apps import AppConfig


class NotificationConfig(AppConfig):
    name = 'notification'

    def ready(self):
        super().ready()
        from .ext_svc_interfacer import ExternalSvcInterfacer
        from .queue_mgr import QueueWriter

        ExternalSvcInterfacer.get_instance(QueueWriter)

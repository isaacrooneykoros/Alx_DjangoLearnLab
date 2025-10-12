from .models import Notification
from django.contrib.contenttypes.models import ContentType

def create_notification(recipient, actor, verb, target=None):
    nt = Notification(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type = ContentType.objects.get_for_model(target) if target else None,
        target_object_id = getattr(target, 'id', None) if target else None,
    )
    nt.save()
    return nt

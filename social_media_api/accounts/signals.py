from django.conf import settings
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .models import User
from notifications.utils import create_notification

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Follow notifications
@receiver(m2m_changed, sender=User.following.through)
def follows_changed(sender, instance, action, pk_set, **kwargs):
    # instance is user making the change; pk_set contains target user ids
    from django.contrib.auth import get_user_model
    UserModel = get_user_model()
    if action == 'post_add':
        for target_id in pk_set:
            target = UserModel.objects.get(pk=target_id)
            if target != instance:
                create_notification(recipient=target, actor=instance, verb='started following you')

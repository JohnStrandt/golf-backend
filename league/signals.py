from django.contrib.auth.models import User
from .models import Player

from core.settings import EMAIL_HOST_USER
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail


# create_user is a two-step process in Django
def createPlayer(sender, instance, created, **kwargs):
    if created:
        user = instance
        player = Player.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        subject = 'Welcome to Tournament Golf'
        message = f'Good luck on the course {user.first_name}!'

        send_mail(
        subject,
        message,
        EMAIL_HOST_USER,
        [player.email],
        fail_silently=False,
        )


#  user changes their info, this is triggered
def updateUser(sender, instance, created, **kwargs):
    player = instance
    user = player.user
    if created == False:
        user.first_name = player.first_name
        user.last_name = player.last_name
        user.username = player.username
        user.email = player.email
        user.save()


def deleteUser(sender, instance, **kwargs):
    # errors are possible when deleting user from Users in admin
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createPlayer, sender=User)
post_save.connect(updateUser, sender=Player)
post_delete.connect(deleteUser, sender=Player)
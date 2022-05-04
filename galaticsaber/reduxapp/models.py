from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="assigned_profile")
    realname = models.CharField(max_length=20, blank=True)

    mtg_currentELO = models.IntegerField(default=1000)
    mtg_highestELO = models.IntegerField(default=1000)
    mtg_lowestELO = models.IntegerField(default=1000)
    lsd_currentELO = models.IntegerField(default=1000)
    lsd_highestELO = models.IntegerField(default=1000)
    lsd_lowestELO = models.IntegerField(default=1000)

    def __str__(self):
        return self.user.username


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class LSDGame(models.Model):
    player1 = models.CharField(max_length=20)
    player2 = models.CharField(max_length=20)
    result = models.FloatField()
    player2ELO = models.IntegerField()
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = str(self.player1) + " VS " + str(self.player2) + " " + str(self.dateTime)
        return name

class MTGGame(models.Model):
    player1 = models.CharField(max_length=20)
    player2 = models.CharField(max_length=20)
    result = models.FloatField()
    player1ELO = models.IntegerField()
    player2ELO = models.IntegerField()
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        name = str(self.player1) + " VS " + str(self.player2) + " " + str(self.dateTime)
        return name


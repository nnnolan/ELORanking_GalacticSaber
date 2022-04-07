import datetime

from django.db import models
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #lightsaber duel elo rating
    class Lsd(models.Model):
        lsd_wins = models.IntegerField(default=0)
        lsd_losses = models.IntegerField(default=0)
        lsd_draws = models.IntegerField(default=0)
        lsd_games = models.IntegerField(default=0)
        lsd_elo = models.IntegerField(default=0)
        lsd_winpercent = models.FloatField(default=0)
    
    #mtg  elo
    class Mtg(models.Model):
        mtg_wins = models.IntegerField(default=0)
        mtg_losses = models.IntegerField(default=0)
        mtg_draws = models.IntegerField(default=0)
        mtg_games = models.IntegerField(default=0)
        mtg_elo = models.IntegerField(default=0)
        mtg_winpercent = models.FloatField(default=0)

    def __str__(self):
        return "%s" % self.username
    # else:
    #     print("error") ## fix this, needs to respond if no login

class lsd_duel(models.Model):
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='lsd_duelist1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='lsd_duelist2')
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    player1_start_rating = models.IntegerField(default=1000)
    player2_start_rating = models.IntegerField(default=1000)
    player1_end_rating = models.IntegerField(default=1000)
    player2_end_rating = models.IntegerField(default=1000)
    date = models.DateTimeField(default=datetime.datetime.now),
    
    def get_winner(self):
        if self.player1_score > self.player2_score:
            return self.player1
        else:
            return self.player2
    
    def __str__(self):
        return "%s vs %s" % (self.player1, self.player2)


class mtg_duel(models.Model):
    player1 = models.ForeignKey(Player, related_name='mtg_duelist1', on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name='mtg_duelist2', on_delete=models.CASCADE)
    player1_score = models.IntegerField(default=0)
    player2_score = models.IntegerField(default=0)
    player1_start_rating = models.IntegerField(default=1000)
    player2_start_rating = models.IntegerField(default=1000)
    player1_end_rating = models.IntegerField(default=1000)
    player2_end_rating = models.IntegerField(default=1000)
    date = models.DateTimeField(default=datetime.datetime.now),
    
    def get_winner(self):
        if self.player1_score > self.player2_score:
            return self.player1
        else:
            return self.player2
    
    def __str__(self):
        return "%s vs %s" % (self.player1, self.player2)
# import datetime

# from django.db import models

# from django.contrib.auth.models import User 


# class Player(models.Model):
#         username = models.CharField(max_length=100)

#         #lightsaber duel elo 
#         lsd_wins = models.IntegerField(default=0)
#         lsd_losses = models.IntegerField(default=0)
#         lsd_draws = models.IntegerField(default=0)
#         lsd_games = models.IntegerField(default=0)
#         lsd_elo = models.IntegerField(default=0)
#         lsd_winpercent = models.FloatField(default=0)
       
#         #mtg  elo
#         mtg_wins = models.IntegerField(default=0)
#         mtg_losses = models.IntegerField(default=0)
#         mtg_draws = models.IntegerField(default=0)
#         mtg_games = models.IntegerField(default=0)
#         mtg_elo = models.IntegerField(default=0)
#         mtg_winpercent = models.FloatField(default=0)

#         def __str__(self):
#             return "%s" % self.username
#     # else:
#     #     print("error") ## fix this, needs to respond if no login

# class lsd_duel(models.Model):
#     player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
#     player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')
#     date = models.DateTimeField(default=datetime.datetime.now)

#     def get_winner(self):
#         if self.player1_score > self.player2_score:
#             return self.player1
#         else:
#             return self.player2
    
#     def __str__(self):
#         return "%s vs %s" % (self.player1, self.player2)

# class mtg_duel(models.Model):
#     player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
#     player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')
#     date = models.DateTimeField(default=datetime.datetime.now)

#     def get_winner(self):
#         if self.player1_score > self.player2_score:
#             return self.player1
#         else:
#             return self.player2
    
#     def __str__(self):
#         return "%s vs %s" % (self.player1, self.player2)
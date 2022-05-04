from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError, models
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings

from .models import MTGGame, LSDGame, Profile

import math


def home(request):
    
    users = User.objects.all()
    mtg_games = MTGGame.objects.all()
    lsd_games = LSDGame.objects.all()


    mtg_games_list = []
    for game in mtg_games:
        mtg_games_list.append(game)

    lsd_games_list = []
    for game in lsd_games:
        lsd_games_list.append(game)


    if request.method == 'GET':
        return render(request, 'reduxapp/home.html', {'users':users, "mtg_games":mtg_games_list, "lsd_games":lsd_games_list})
    elif not username_present(request.POST['player1']):
        return render(request, 'reduxapp/home.html', {'users':users, 'error1':'Can not find Player 1.', "mtg_games":mtg_games_list, "lsd_games":lsd_games_list})

    elif not username_present(request.POST['player2']):
        return render(request, 'reduxapp/home.html', {'users':users, 'error2':'Can not find Player 2.', "mtg_games":mtg_games_list, "lsd_games":lsd_games_list})

    else:

        # user1 = Profile.objects.get_or_create(user=request.user)

        user1 = User.objects.get(username=request.POST['player1'])
        user2 = User.objects.get(username=request.POST['player2'])
        print(user1, user2) # DEBUG LINE -- it does find
        print(user1.assigned_profile.mtg_currentELO) # DEBUG LINE -- it does NOT FIND
        '''
        the iissue is finding the user via user.profile , not user.x.y.z
        '''
        mtg_or_lsd = float(request.POST['mtg_or_lsd']) #mtg = 1, lsd = 2; assigned from the home.html
        outcome = float(request.POST['outcome']) #1 = player 1 won, 0 = player 2 won


        if mtg_or_lsd == 1: #mtg game
            '''
            i think the problem is arising from the fact that user is a
            a method of the class Profile, as opposed to be a way of finding
            the user. 
            '''
            user1new, user2new = GameELO(user1.assigned_profile.mtg_currentELO, user2.assigned_profile.mtg_currentELO, outcome)
            user1change = user1new - user1.assigned_profile.mtg_currentELO
            user2change = user2new - user2.assigned_profile.mtg_currentELO

            save_mtg_game(user1, user2, outcome) #true means magic game

        else: #lsd game
            user1new, user2new = GameELO(user1.assigned_profile.lsd_currentELO, user2.assigned_profile.lsd_currentELO, outcome)
            user1change = user1new - user1.assigned_profile.lsd_currentELO
            user2change = user2new - user2.assigned_profile.lsd_currentELO
            save_lsd_game(user1, user2, outcome) #false means LSD

        gamedata = {'user1': user1,
                    'user2': user2,
                    'mtg_or_lsd': mtg_or_lsd,
                    'outcome': outcome,
                    'user1change': user1change,
                    'user2change': user2change}

        if gamedata['mtg_or_lsd'] == 1: #mtg  or lsd stuff
            gamedata['mtg_or_lsd'] = "MTG"
        else:
            gamedata['mtg_or_lsd'] = "Lightsaber Duel"

        if gamedata['outcome'] == True: # seeing who wun
            gamedata['message'] = 'Player 1 won.'
        elif gamedata['outcome'] == False:
            gamedata['message'] = 'Player 2 won.'
        else:
            gamedata['outcome'] = 'Game was draw.'




        return render(request, 'reduxapp/gameadded.html', {'gamedata':gamedata, "mtg_games":mtg_games_list, "lsd_games":lsd_games_list})


def createuser(request):
    # Check if coming first time
    if request.method == 'GET':
        return render(request, 'reduxapp/createuser.html')
    else:
        try:
            user = User.objects.create_user(request.POST.get['username'])
            user.save()
            return redirect('home')

        except IntegrityError:
            return render(request, 'reduxapp/createuser.html', {'error':'That username has already been taken'})


def lsd_ranking(request):
    # COME BACK TO THIS
    # users = User.objects.all().order_by('profile.currentELO')
    profiles = Profile.objects.all().order_by('-lsd_currentELO')[:10]
    ranking = []
    i = 1
    for profile in profiles:

        rank = str(i) + ". " + profile.user.username + " (" + str(profile.currentELO) +")"
        ranking.append(rank)
        i += 1
    return render(request, 'reduxapp/ranking.html', {'ranking':ranking})


def playersearch(request):
    if request.method == 'GET':
        return render(request, 'reduxapp/playersearch.html')
    else:
        user = User.objects.get(username=request.POST['search'])
        return redirect('playerpage', user.id)


def playerpage(request, user_pk):
    user, created = User.objects.get_or_create(user=request.user)
    # user = get_object_or_404(User, pk=user_pk)
    mtg_games = MTGGame.objects.all()
    lsd_games = LSDGame.objects.all()
    if request.method == 'GET':
        data = [1000]
        date = [str(user.date_joined.strftime("%d.%m.%Y"))]
        opponent = []

        for game in mtg_games:
            white = get_object_or_404(User, username=game.player1)
            black = get_object_or_404(User, username=game.player2)

            if game.player1 == user.username:
                data.append(GameELO(game.player1ELO, game.player2ELO, game.result))
                date.append(str(game.dateTime.strftime("%d.%m.%Y")))
                opponent.append(game.player2)

            elif game.player2 == user.username:
                data.append(GameELO(game.player1ELO, game.player2ELO, game.result))
                date.append(str(game.dateTime.strftime("%d.%m.%Y")))
                opponent.append(game.player1)


        return render(request, 'reduxapp/playerpage.html', {'user':user, 'data':data, 'date':date})

"""
def dataToVisuals(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)

    data = []
    date = []
    opponent = []

    for game in Game:
        if game.player1 == user.username:
            data.append(GameELOWhite(game.player1, game.player2, game.result))
            date.append(game.dateTime)
            opponent.append(game.player2)

        elif game.player2 == user.username:
            data.append(int(GameELOWhite(game.player1, game.player2, game.result)))
            date.append(str(game.dateTime))
            opponent.append(str(game.player1))

    return JsonResponse(data={
        'data': data,
        'date': date,
        'opponent': opponent,
    })
"""


def save_mtg_game(player1, player2, result):
    

    game = MTGGame(player1=player1.assigned_profile.username, player2=player2.assigned_profile.username, result=result, player1ELO=player1.assigned_profile.lsd_currentELO, player2ELO=player1.assigned_profile.lsd_currentELO)
    # game.save()

#profile stuff
    player1.assigned_profile.mtg_currentELO, player2.assigned_profile.mtg_currentELO = GameELO(player1.profile.mtg_currentELO, player2.profile.mtg_currentELO, result)
    if player1.assigned_profile.mtg_currentELO > player1.assigned_profile.mtg_highestELO:
        player1.assigned_profile.mtg_highestELO = player1.assigned_profile.mtg_currentELO

    if player2.assigned_profile.mtg_currentELO > player2.assigned_profile.mtg_highestELO:
        player2.assigned_profile.mtg_highestELO = player2.assigned_profile.mtg_currentELO

    if player1.assigned_profile.mtg_currentELO < player1.assigned_profile.mtg_lowestELO:
        player1.assigned_profile.mtg_lowestELO = player1.assigned_profile.mtg_currentELO

    if player2.assigned_profile.mtg_currentELO < player2.assigned_profile.mtg_lowestELO:
        player2.assigned_profile.mtg_lowestELO = player2.assigned_profile.mtg_currentELO

    player1.save()
    player2.save()

    return

def save_lsd_game(player1, player2, result):


    game = LSDGame(player1=player1.assigned_profile.username, player2=player2.assigned_profile.username, result=result, player1ELO=player1.assigned_profile.lsd_currentELO, player2ELO=player2.assigned_profile.lsd_currentELO)
    game.save()

    player1.assigned_profile.lsd_currentELO, player2.assigned_profile.lsd_currentELO = GameELO(player1.profile.lsd_currentELO, player2.profile.lsd_currentELO, result)
    if player1.assigned_profile.lsd_currentELO > player1.assigned_profile.lsd_highestELO:
        player1.assigned_profile.lsd_highestELO = player1.assigned_profile.lsd_currentELO

    if player2.assigned_profile.lsd_currentELO > player2.assigned_profile.lsd_highestELO:
        player2.assigned_profile.lsd_highestELO = player2.assigned_profile.lsd_currentELO

    if player1.assigned_profile.lsd_currentELO < player1.assigned_profile.lsd_lowestELO:
        player1.assigned_profile.lsd_lowestELO = player1.assigned_profile.lsd_currentELO

    if player2.assigned_profile.lsd_currentELO < player2.assigned_profile.lsd_lowestELO:
        player2.assigned_profile.lsd_lowestELO = player2.assigned_profile.lsd_currentELO

    player1.save()
    player2.save()

    return


def GameELO(rating1, rating2, result):

    # Probabilities of winning
    prob_rating1 = 1/(1+10 ** ((rating2-rating1)/400))
    prob_rating2 = 1/(1+10 ** ((rating1-rating2)/400))


    if result == 1:
        rating1 += 32 * (1-prob_rating1)
        rating2 += 32 * (0-prob_rating2)
    
    else:
        rating1 += 32 * (0-prob_rating1)
        rating2 += 32 * (1-prob_rating2)

    return rating1, rating2




# def GameELO(rating1, rating2, result):
#     # Probabilities of winning
#     prob_rating1 = 1/(1+10 ** ((rating2-rating1)/400))

#     # Adjusting ELO rantings
#     rating1 += 32*(result - prob_rating1)

#     return rating1, rating2


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False
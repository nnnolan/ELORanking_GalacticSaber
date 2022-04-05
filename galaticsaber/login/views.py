import math

from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Player, mtg_duel, lsd_duel

# Create your views here.

def home(request):
    return render(request, "login/home.html")

def leaderboard(request):
    return render(request, "login/leaderboard.html")

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def forgot_password(request):
    return render(request, "registration/forgot-password.html")


login_required
def new_game(request):
    players = Player.objects.all().order_by('name')
    # If it isn't a post, we are just going to display the game entry form
    if request.method != 'POST':
        return render(request, 'foos/game.html', {
            'players' : players,
        })

    else:
        try:
            game_type = request.POST['game_type']
        except KeyError:
            return render(request, 'foos/game.html', {
                'error_message' : 'Invalid POST received! Clown.',
                'players' : players
            })

        # Singles game entry
        result = None
        if game_type == "mtg":
            result = _validate_and_submit_singles_post(request)
        elif game_type == "doubles":
            result = _validate_and_submit_doubles_post(request)
        else:
            return render(request, 'foos/game.html', {
                'error_message' : 'Invalid game_type received! Clown.',
                'players' : players,
                'teams' : teams,
            })

        if result:
            if result['error']:
                return render(request, 'foos/game.html', {
                    'error_message' : result['error_message'],
                    'players' : players,
                    'teams' : teams,
                })

        # Whew! Okay, the result looks valid.
        return redirect('foos:index')


@login_required
def player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    # Pull a list of all games played by the player
    singles_games = SinglesGame.objects\
        .filter(Q(player1=player) | Q(player2=player))\
        .order_by('-date')
    processed_singles_games = []
    for game in singles_games:
        setattr(game, 'player1_rating_change',
                game.player1_end_rating - game.player1_start_rating)
        setattr(game, 'player2_rating_change',
                game.player2_end_rating - game.player2_start_rating)
        processed_singles_games.append(game)
    # Build a list of wins/losses vs. every other player
    prob_player_list = _calculate_player_win_probs(player_id)
    # Build probability of winning vs every other player
    return render(request, 'foos/player.html', {
        'player' : player,
        'singles_games' : processed_singles_games,
        'player_probabilities' : prob_player_list
    })


# def forgot_password(request):
#     return render(request, "login/forgot-password.html")


# @login_required
# def player(request)
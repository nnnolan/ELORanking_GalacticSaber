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

# def player(request, player_id):
#     return render("login/player.html")

@login_required
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
            result = _validate_and_submit_lsd_post(request)
        elif game_type == "lsd":
            result = _validate_and_submit_mtg_post(request)
        else:
            return render(request, 'foos/game.html', {
                'error_message' : 'Invalid game_type received! Clown.',
                'players' : players,
            })

        if result:
            if result['error']:
                return render(request, 'foos/game.html', {
                    'error_message' : result['error_message'],
                    'players' : players,
                })

        # Whew! Okay, the result looks valid.
        return redirect('foos:index')


@login_required
def player(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    # Pull a list of all games played by the player
    singles_games = mtg_duel.objects\
        .filter(Q(player1=player) | Q(player2=player))\
        .order_by('-date')
    lsd_games = mtg_duel.objects\
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
    return render(request, 'login/player.html', {
        'player' : player,
        'singles_games' : processed_singles_games,
        'player_probabilities' : prob_player_list
    })

def _calculate_player_win_probs(player_id):
    player = Player.objects.get(id=player_id)
    other_players = Player.objects.exclude(id=player_id)
    results = []
    for other in other_players:
        # Calculate the wins and losses vs. each player
        wins = 0
        losses = 0
        singles1 = mtg_duel.objects.filter(player1=player, player2=other)
        for game in singles1:
            if game.player1_score > game.player2_score:
                wins += 1
            elif game.player2_score > game.player1_score:
                losses += 1
        singles2 = mtg_duel.objects.filter(player1=other, player2=player)
        for game in singles2:
            if game.player1_score > game.player2_score:
                losses += 1
            elif game.player2_score > game.player1_score:
                wins += 1

        # Now calculate the probability of victory based on the rating
        # compared to the other player
        rating_difference = player.rating - other.rating
        base_prob = 1 / (1 + math.pow(10, (rating_difference / 400)))
        probability = 1 - base_prob
        probability = round(probability * 100, 1)
        player_obj = {
            'name' : other.name,
            'probability' : probability,
            'rating' : other.rating,
            'id' : other.id,
            'wins' : wins,
            'losses' : losses,
        }
        results.append( player_obj )

    return results

def _calculate_elo(player_rating, opponent_rating, player_score, opponent_score):
    # sa = actual score
    # ea = expected score

    if player_score < opponent_score:
        sa = 0
    if player_score > opponent_score:
        sa = 1
    if player_score == opponent_score:
        sa = 0.5
    ea = 1 / (1 + math.pow(10, ((opponent_rating - player_rating) / 400)))

    # k = "k-factor"
    k = 32
    if player_rating > 2100 and player_rating < 2400:
        k = 24
    if player_rating > 2400:
        k = 16

    new_rating = player_rating + k * (sa - ea)
    return round(new_rating)

def _validate_and_submit_mtg_post(request):
    return_data = {
        'error' : False,
        'error_message' : '',
        'status_message' : '',
    }

    try:
        player1_id = request.POST['player1']
        player2_id = request.POST['player2']
        player1_score = request.POST['player1_score']
        player2_score = request.POST['player2_score']
    except KeyError:
        return_data['error_message'] = 'Invalid POST received! Clown.'
        return_data['error'] = True
        return return_data

    # Make sure the same player isn't selected
    if player1_id == player2_id:
        return_data['error_message'] = 'You selected the same player! Clown.'
        return_data['error'] = True
        return return_data

    if player1_score == '' or player1_score is None:
        player1_score = 0
    if player2_score == '' or player2_score is None:
        player2_score = 0
    try:
        player1_score = int(player1_score)
        player2_score = int(player2_score)
    except Exception:
        return_data['error_message'] = 'Player score must be an integer! Clown.'
        return_data['error'] = True
        return return_data
    try:
        player1_id = int(player1_id)
        player2_id = int(player2_id)
    except Exception:
        return_data['error_message'] = "Don't try to submit weird data! Clown."
        return_data['error'] = True
        return return_data

    player1 = Player.objects.get(id=player1_id)
    player2 = Player.objects.get(id=player2_id)

    if not player1 and not player2:
        return_data['error_message'] = "Players do not exist! Clown."
        return_data['error'] = True
        return return_data

    # Check the scores to make sure they are in the range of 0-11
    if player1_score < 0 or player1_score > 11:
        return_data['error_message'] = 'Player 1 score was outside the range of 0-11! Clown.'
        return_data['error'] = True
        return return_data
     # Check the scores to make sure they are in the range of 0-11
    if player2_score < 0 or player2_score > 11:
        return_data['error_message'] = 'Player 2 score was outside the range of 0-11! Clown.'
        return_data['error'] = True
        return return_data
    # House rules. If a tiebreaker (win by 2) happened, the winning score must be 11-9.
    if player1_score == 11 or player2_score == 11:
        if player1_score != 9 and player2_score != 9:
            return_data['error_message'] = 'If win-by-two (tiebreaker), the resulting score must be 11-9!'
            return_data['error'] = True
            return return_data
    # House rules, cannot win by 1.
    if player1_score == 10 or player2_score == 10:
        if player1_score == 9 or player2_score == 9:
            return_data['error_message'] = 'If win-by-two (tiebreaker), the resulting score must be 11-9!'
            return_data['error'] = True
            return return_data

    if player1_score != 10 and player2_score != 10 and player1_score != 11 and player2_score != 11:
        if player1_score - player2_score != 0:
            return_data['error_message'] = 'Surely somebody won the game?'
            return_data['error'] = True
            return return_data

    p1_end_rating = _calculate_elo(player1.rating, player2.rating, player1_score, player2_score)
    p2_end_rating = _calculate_elo(player2.rating, player1.rating, player2_score, player1_score)

    s = mtg_duel(
        player1=player1,
        player2=player2,
        player1_score=player1_score,
        player2_score=player2_score,
        player1_start_rating=player1.rating,
        player2_start_rating=player2.rating,
        player1_end_rating=p1_end_rating,
        player2_end_rating=p2_end_rating,
    )
    s.save()

    if player1_score > player2_score:
        player1.mtg_wins += 1
        player2.mtg_losses += 1
    elif player2_score > player1_score:
        player2.mtg_wins += 1
        player1.mtg_losses += 1
    else:
        player1.mtg_draws += 1
        player2.mtg_draws += 1

    player1.mtg_games += 1
    player2.mtg_games += 1

    # Update ratings
    player1.mtg_elo = p1_end_rating
    player2.mtg_elo = p2_end_rating
    player1.save()
    player2.save()

    return return_data
    


def _validate_and_submit_lsd_post(request):
    return_data = {
        'error' : False,
        'error_message' : '',
        'status_message' : '',
    }

    try:
        player1_id = request.POST['player1']
        player2_id = request.POST['player2']
        player1_score = request.POST['player1_score']
        player2_score = request.POST['player2_score']
    except KeyError:
        return_data['error_message'] = 'Invalid POST received! Clown.'
        return_data['error'] = True
        return return_data

    # Make sure the same player isn't selected
    if player1_id == player2_id:
        return_data['error_message'] = 'You selected the same player! Clown.'
        return_data['error'] = True
        return return_data

    if player1_score == '' or player1_score is None:
        player1_score = 0
    if player2_score == '' or player2_score is None:
        player2_score = 0
    try:
        player1_score = int(player1_score)
        player2_score = int(player2_score)
    except Exception:
        return_data['error_message'] = 'Player score must be an integer! Clown.'
        return_data['error'] = True
        return return_data
    try:
        player1_id = int(player1_id)
        player2_id = int(player2_id)
    except Exception:
        return_data['error_message'] = "Don't try to submit weird data! Clown."
        return_data['error'] = True
        return return_data

    player1 = Player.objects.get(id=player1_id)
    player2 = Player.objects.get(id=player2_id)

    if not player1 and not player2:
        return_data['error_message'] = "Players do not exist! Clown."
        return_data['error'] = True
        return return_data

    # Check the scores to make sure they are in the range of 0-11
    if player1_score < 0 or player1_score > 11:
        return_data['error_message'] = 'Player 1 score was outside the range of 0-11! Clown.'
        return_data['error'] = True
        return return_data
     # Check the scores to make sure they are in the range of 0-11
    if player2_score < 0 or player2_score > 11:
        return_data['error_message'] = 'Player 2 score was outside the range of 0-11! Clown.'
        return_data['error'] = True
        return return_data
    # House rules. If a tiebreaker (win by 2) happened, the winning score must be 11-9.
    if player1_score == 11 or player2_score == 11:
        if player1_score != 9 and player2_score != 9:
            return_data['error_message'] = 'If win-by-two (tiebreaker), the resulting score must be 11-9!'
            return_data['error'] = True
            return return_data
    # House rules, cannot win by 1.
    if player1_score == 10 or player2_score == 10:
        if player1_score == 9 or player2_score == 9:
            return_data['error_message'] = 'If win-by-two (tiebreaker), the resulting score must be 11-9!'
            return_data['error'] = True
            return return_data

    if player1_score != 10 and player2_score != 10 and player1_score != 11 and player2_score != 11:
        if player1_score - player2_score != 0:
            return_data['error_message'] = 'Surely somebody won the game?'
            return_data['error'] = True
            return return_data

    p1_end_rating = _calculate_elo(player1.rating, player2.rating, player1_score, player2_score)
    p2_end_rating = _calculate_elo(player2.rating, player1.rating, player2_score, player1_score)

    l = lsd_duel(
        player1=player1,
        player2=player2,
        player1_score=player1_score,
        player2_score=player2_score,
        player1_start_rating=player1.rating,
        player2_start_rating=player2.rating,
        player1_end_rating=p1_end_rating,
        player2_end_rating=p2_end_rating,
    )
    l.save()

    if player1_score > player2_score:
        player1.lsd_wins += 1
        player2.lsd_losses += 1
    elif player2_score > player1_score:
        player2.lsd_wins += 1
        player1.lsd_losses += 1
    else:
        player1.lsd_draws += 1
        player2.lsd_draws += 1

    player1.lsd_games += 1
    player2.lsd_games += 1

    # Update ratings
    player1.lsd_rating = p1_end_rating
    player2.lsd_rating = p2_end_rating
    player1.save()
    player2.save()

    return return_data


# def forgot_password(request):
#     return render(request, "login/forgot-password.html")


# @login_required
# def player(request)
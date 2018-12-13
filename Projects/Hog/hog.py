"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total = 0 #This is the total that will be returned at the end
    is_there_one = False #This is an indicator whether any of the dice outcome is 1
    while num_rolls > 0:
        #'current_outcome' is the outcome of the dice in 1 roll
        current_outcome = dice()
        #If any of the current_outcome is 1, then make is_there_one True
        if current_outcome == 1:
            is_there_one = True
        #Accumulate all the dice outcome
        total += current_outcome 
        #Reduce num_rolls by 1 every time the iteration cycles
        num_rolls -= 1
    #If is_there_one returns True, change the 'total' to 1
    if is_there_one:
        total = 1
    return total
        
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    return 2 + abs(score//10 - score%10)
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    if num_rolls == 0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def is_swap(score0, score1):
    """Return whether one of the scores is an integer multiple of the other."""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    #Make sure both score0 and score 1 is greater than 1
    if score0 > 1 and score1 > 1:
        #Case 1: if If player 0's score is greater than player 1's score and they are divisible to each other
        if score0 > score1:
            return score0 % score1 == 0
        # Case 2: Other way around
        elif score1 > score0:
            return score1 % score0 == 0
    #If the scores do not fulfill any of the above, return False
    return False
    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    #While both players' score are below the goal
    while score0 <goal and score1<goal:
        if player == 0: #If it's player 0's turn
            #Implement take turn 
            score0 += take_turn(strategy0(score0,score1),score1,dice)
        else: #If it's player 1's turn
            score1 += take_turn(strategy1(score1,score0),score0,dice)
        if is_swap(score0,score1):
            score0, score1 = score1, score0
        #======================== BEGIN PROBLEM 6 =====================
        # A commentary function 'say' is called at the end of each turn. 
        # The return value of calling 'say' function is the commentary function
        # to call on the next turn
        say=say(score0,score1)
        # ======================= END PROBLEM 6 ======================= 
        player = other(player) #Switch turn
    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores

def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say

def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 18) # Player 0 gets 8 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 18
    Player 1 takes the lead by 12
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(11, 0)
    >>> f2 = f1(11, 1)
    1 point! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 1)
    >>> f4 = f3(5, 20) # Player 1 gets 4 points, then Swine Swap applies
    19 points! That's the biggest gain yet for Player 1
    >>> f5 = f4(20, 40) # Player 0 gets 35 points, then Swine Swap applies
    20 points! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 55) # Player 1 gets 15 points; not enough for a new high
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def helper(score0, score1):
        sentence = "That's the biggest gain yet for Player "
        if who == 0:
            #If who = 0, then this function refers to player 0
            #set 'current_score' as score0
            current_score = score0
        else:
            #If who = 1, then refers to player 1
            current_score = score1
        difference = current_score - previous_score
        if difference > previous_high:
            #If difference = 1, then there will be no 's' at the end of 'point'
            # If difference is other than one, then there will be 's' at the end of 'points'
            print(str(difference) + ' point' + 's'*(1-(1//difference)) + '! ' + sentence + str(who))
            #recursive call announce_highest, but this time previous_high = difference and previous_score = current score
            return announce_highest(who, difference, current_score)
        #If difference < previous_high, recursive call but only with previous_score = current score
        return announce_highest(who, previous_high, current_score)
    return helper
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

"""==================== HINT FROM ok -q 08 -u =================
1. 'make_averaged' is a higher-order function because it both:
    - takes in a function as an argument and
    - returns a function
2. The function passed into make_averaged takes an arbitrary amount of arguments, which
    is why we need to use *args to call it"""

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0

    From the doctest above,
    1. Every cycle of dice consists of 4 calls, so there are a total of 1000/4 = 250 cycle
    2. The total of make_test_dice is 12, and thus total score is 12 * 250 cycles = 3000
    3. Since there are 1000 dice rolls in total, the average is 3000/1000 = 3.0
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def helper(*args):
        #total is the total score
        #rolls is how many times you have rolled the dice
        total, rolls = 0, 0
        #while the number of dice rolls is still less than the num_samples
        while rolls < num_samples:
            #increment 'total' with the outcome from calling fn with (*args) as the arguments
            total += fn(*args)
            #increase rolls by 1
            rolls += 1
        #the helper function returns the average by dividing total with rolls
        return total / rolls
    return helper
    # END PROBLEM 8

"""================= HINTS FROM ok -q 09 -u ================
If multiple num_rolls are tied for the highest scoring average, we return the lowest num_rolls

>>> from hog import *
>>> dice = make_test_dice(3)   # dice always returns 3
>>> max_scoring_num_rolls(dice, num_samples=1000)
10

>>> from hog import *
>>> dice = make_test_dice(2)     # dice always rolls 2
>>> max_scoring_num_rolls(dice, num_samples=1000)
10
"""

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    #curr_dice is the current number of dice (from 1 to 10) that's being used
    #curr_highest is the currently highest average turn score
    curr_dice, curr_highest = 1, 0
    while curr_dice <= 10:
        helper = make_averaged(roll_dice, num_samples)
        #obtain the current_avg using the helper function
        current_avg = helper(curr_dice, dice)
        #If the current_avg is greater than the curr_highest, updates
        # the curr_highest
        if current_avg > curr_highest:
            curr_highest = current_avg
            #max_scoring_dices is going to be the number of dice that gives the
            # highest average turn score
            max_scoring_dices = curr_dice
        curr_dice += 1
    return max_scoring_dices
            
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.

    ============ HINT FROM ok -q 10 -u ============
    >>> bacon_strategy(0, 0, margin=8, num_rolls=5)
    5
    >>> bacon_strategy(70, 50, margin=8, num_rolls=5)
    5
    >>> bacon_strategy(50, 70, margin=8, num_rolls=5)
    0

    """
    # BEGIN PROBLEM 10
    #If the result of free_bacon of the opponent score is less than margin
    if free_bacon(opponent_score) < margin:
        #then return num_rolls
        return num_rolls
    #else if the result of free_bacon is greater than margin
    else:
        #then do the free_bacon!
        return 0
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.

    ================ HINT FROM ok -q 11 -u =============
    >>> swap_strategy(12, 60, 8, 6)
    0

    >>> swap_strategy(30, 54, 8, 6)
    6

    In the first example, if we roll 0, then we'll get dice outcome of (6-0) + 2 = 8
    and thus, the current score would become 20. 20 and 60 is a beneficial swap.

    In the second example, if we roll 0, we'll get dice outcome of (5-4) + 2 = 3
    and thus, the current score would become 33. 54 is not divisible by 33 and 
    thus, it's not a beneficial swap. 3 is also below the margin, 8.
    """
    # BEGIN PROBLEM 11
    # score_plus_bacon is the current score + the outcome if we got free bacon 
    score_plus_bacon = score + free_bacon(opponent_score)
    # if the opponent score is divisible by score_plus_zero (beneficial swap)
    if opponent_score % score_plus_bacon == 0 and opponent_score > score_plus_bacon:
        return 0
    # If the outcome of free bacon is greater or equal to margin
    elif free_bacon(opponent_score) >= margin:
        return 0
    # Otherwise, return num_rolls
    else:
        return num_rolls


    # END PROBLEM 11


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    return 4  # Replace this statement
    # END PROBLEM 12


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
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
    total = 0 # Total final score that will be returned in the end
    is_there_one = False # An indicator for whether any of the dice outcome is 1
    while num_rolls > 0:
        current_outcome = dice() # The outcome of the current roll
        if current_outcome == 1: # If any of the current roll outcome is 1, then the indicator becomes True
            is_there_one = True
        total += current_outcome # Increment total with the outcome of current roll
        num_rolls -= 1 # Decrement num_rolls by 1 for every while cycle

    if is_there_one: # If the indicator is True, then at the end, we change 'total' to 1
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
    # score // 10 returns the 2nd digit of the score
    # score % 10 returns the first digit of the score
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
    # With what have been implemented so far, the score outcome of a player turn can be obtained by either
    # a normal dice roll or rolling 0 dice (free bacon)
    if num_rolls == 0: # If current player rolls zero dice
        return free_bacon(opponent_score) # return the result of calling free_bacon on opponent's score
    else:
        return roll_dice(num_rolls, dice) # Otherwise, just return the result of normal dice roll
    # END PROBLEM 3


def is_swap(score0, score1):
    """Return whether one of the scores is an integer multiple of the other."""
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"

    # The Swine Swap occurs if both players' score are greater than 1 AND
    # the greater score has to be divisible by the lesser score

    if score0 > 1 and score1 > 1:
        return score0 % score1 == 0 or score1 % score0 == 0
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
    player = 0  # Initially start with player 0's turn
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    # ======== PSEUDO CODE ======= #
    # - While both players' scores are below goal:
    #   - For a particular player's turn, increment that player's score by the amount returned from calling take_turn
    #   - Check for is_swap condition. If it's fulfilled, swap both players' score
    #   - Switch player turn
    # - Outside the while loop, return both players' score

    while score0 <goal and score1<goal:
        if player == 0: #If it's player 0's turn
            score0 += take_turn(strategy0(score0,score1),score1,dice) # Increment player 0's turn by take_turn
        else: #If it's player 1's turn
            score1 += take_turn(strategy1(score1,score0),score0,dice) # Increment player 1's turn by take_turn
        if is_swap(score0,score1): # Check is_swap condition
            score0, score1 = score1, score0 # If is_swap is fulfilled, then swap both players' scores
        #======================== BEGIN PROBLEM 6 =====================
        # The 'say' function prints a commentary remarks then returns another commentary function that takes
        # the same number of arguments as 'say'. This 'other' commentary function also prints a commentary remarks
        # and returns another commentary function. It's a repeated cycle.
        say=say(score0,score1)
        # ======================= END PROBLEM 6 ======================= 

        player = other(player) #Switch player turn
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
    def say(score0, score1):
        # Determine whose score we are keeping track of. If who is 0,
        # we keep track of Player 0's. Otherwise, Player 1.
        if who == 0:
            current_score = score0
        else:
            current_score = score1

        current_gain = current_score - previous_score
        part_announce = "That's the biggest gain yet for Player " # Placeholder announcement sentence
        if current_gain > previous_high:
            # The 's' * (1 - (1 // current_gain)) is a tricky method of deciding whether the gain is 1 or not.
            # If the gain is 1, then (1 - (1 // 1)) = (1 - 1) = 0, and thus the 's' is multiplied by 0
            # Otherwise, (1 - (1 // [other number])) is 1, and thus the output will include 's'
            print("{} point{}! {}{}".format(current_gain, 's' * (1 - (1 // current_gain)), part_announce, who))

            return announce_highest(who, current_gain, current_score)
        return announce_highest(who, previous_high, current_score)
    return say
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

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """

    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    def helper(*args):
        total = 0 # Keeps track of the total score so far
        for i in range(num_samples): 
            total += fn(*args) # Increment total by the result of calling fn num_rolls times
        return total / num_samples
    return helper
    # END PROBLEM 8

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
    max_dice = 0
    currentmax_avg = 0
    for i in range(1, 11):
        current_avg = make_averaged(roll_dice, num_samples)(i, dice)
        if current_avg > currentmax_avg:
            max_dice = i
            currentmax_avg = current_avg
    return max_dice

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
    """
    # BEGIN PROBLEM 10
    # Simply check if the result of calling free_bacon on opponent_score is equal to or greater than margin
    if free_bacon(opponent_score) >= margin:
        return 0
    else:
        return num_rolls
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    total_score = score + free_bacon(opponent_score)
    # If the opponent_score is divisible by total_score and the opponent_score is greater than total_score, or 
    # if free_bacon(opponent_score) is equal to or greater than the margin, then roll 0
    if (opponent_score % total_score == 0 and opponent_score > total_score) or free_bacon(opponent_score) >= margin:
        return 0
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
# The Game of Hog
![dice](https://inst.eecs.berkeley.edu/~cs61a/fa18/proj/hog/images/die5.gif)

## Introduction

Simulation of [dice game Pig](https://en.wikipedia.org/wiki/Pig_(dice_game)). This project is based on [University of California Berkeley CS61A Spring 2018 Project 1: The Game of Hog](https://inst.eecs.berkeley.edu/~cs61a/sp18/proj/hog/). This project is focused on the application of control statements and higher-order functions.

In this game, two players compete each other to be the first to reach 100 points or greater by alternating turns to roll dice. On each turn, a player can roll up to 10 dice, and that player's score for the turn is the sum of the dice outcome.

The rule of the game is as the following:

### Pig Out
If any of the dice outcome is a 1, the player's score for that turn is 1. Some example situations:
1. Player 1 rolls 7 dice, one of them has an outcome of 1. Player 1 scores 1 point for that turn.
2. Player 1 rolls 2 dice, one of them is 4, and out of them is 6. Since **Pig Out** does not apply, Player 1 scores 10 points for that turn. 

### Free Bacon
If a player chooses to roll no dice at all, the player scores `2 * [absolute difference between the digits in the opponent's total score` on that turn. Some example situations:
1. If Player 2 has 42 points and Player 1 chooses to roll no dice at all, Player 1 gains `2 + |4 - 2|` = 4
2. If Player 2 has 7 points and Player 1 chooses to roll no dice at all, Player 1 gains `2 + |0 - 7|` = 9

### Swine Swap
After a player's turn is over, if both players' score are greater than 1 and one player's score is a positive integer multiple of the other, then both players' scores are swapped. Some example situations:
1. Player 1 has a score of 37 while Player 2 has 92. Player 1 then takes a turn and scores 9. Now Player 1 has 46 while Player 2 has 92. Since 92 is a multiple of 46, then both players' scores are then swapped! Player 1 now has 92 points, while Player 2 has 46.
2. Player 1 has a score of 91 points while Player 2 has 37. Player 1 then takes a turn and scores 20. Player 1's score is now 111, which is a multiple of 37, therefore both players' scores are swapped! Since Player 2's score is now 111, Player 2 wins the game.

## Instruction on How to Run the Game
Using terminal or shell, navigate to `/Hog` main directory and run
 ```
 python hog_gui.py
 ```
 or 
 ```
 python3 hog_gui.py
 ``` 
 
 depending on which Python version you have.


## Files and Directories

My personal implementations are as the following:
* `hog.py`: my implementation of the game logic and engine
* `jupyter`: directory containing Jupyter notebook files. The notebook explains my code in more details

Supplemental files and directories that come with the project package:
* `dice.py`: Functions for rolling dice
* `hog_gui.py`: A graphical user interface for Hog
* `ucb.py`: Utility functions for CS61A
* `ok`: CS61A autograder
* `tests`: A directory of tests used by `ok`
* `images`: A directory of images used by `hog_gui.py`



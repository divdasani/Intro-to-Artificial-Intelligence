from __future__ import print_function
# File: Player.py
# Author(s) names AND netid's:
# Date:
# Group work statement: <please type the group work statement
#      given in the pdf here>
# Defines a simple artificially intelligent player agent
# You will define the alpha-beta pruning search algorithm
# You will also define the score function in the MancalaPlayer class,
# a subclass of the Player class.


from builtins import str
from builtins import input
from builtins import object
from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player(object):
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    # You will write the score function in the MancalaPlayer below
    # to improve on this function.
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0

    # You should not modify anything before this point.
    # The code you will add to this file appears below this line.

    # You will write this function (and any helpers you need)
    # You should write the function here in its simplest form:
    #   1. Use ply to determine when to stop (when ply == 0)
    #   2. Search the moves in the order they are returned from the board's
    #       legalMoves function.
    # However, for your custom player, you may copy this function
    # and modify it so that it uses a different termination condition
    # and/or a different move search order.
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        print("Alpha Beta Move not yet implemented")
        #returns the score adn the associated moved
        return (-1,1)
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = eval(input("Please enter your move:"))
            while not board.legalMove(self, move):
                print(move, "is not valid")
                move = eval(input( "Please enter your move" ))
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print("chose move", move)
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print("chose move", move, " with value", val)
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print("chose move", move, " with value", val)
            return move
        elif self.type == self.CUSTOM:
            # TODO: Implement a custom player
            # You should fill this in with a call to your best move choosing
            # function.  You may use whatever search algorithm and scoring
            # algorithm you like.  Remember that your player must make
            # each move in about 10 seconds or less.
            print("Custom player not yet implemented")
            return -1
        else:
            print("Unknown player type")
            return -1


# Note, you should change the name of this player to be your netid
class dmd8603(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def __init__(self, playerNum, playerType, ply=6):
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply



    def score(self, board):
        #How many stones I have more than opponent, negative if I have less
        myScore = board.scoreCups[0]
        oppScore = board.scoreCups[1]

        for pit in range(board.NCUPS):
            # I will value each stone on my side as 0.5 (half), unless the opposite pit is empty in which case I value it 0.25 (quarter)
            # Opposite pit will be equal to (5-current pit)
            if (board.P2Cups[5-pit] == 0):
                myScore += (board.P1Cups[pit])*0.4
            else:
                myScore += (board.P1Cups[pit]) * 0.8
            # I will give same value for opponent's stones but reduce the effective score by that amount
            if (board.P1Cups[5-pit] == 0):
                oppScore += (board.P2Cups[pit])*0.4
            else:
                oppScore += (board.P2Cups[pit]) * 0.8
            # If the pit number plus the stones in the pit = 6, than that pit will give us extra turn
            # If I have potential for extra turn, than add 1 to score
            if (pit + board.P1Cups[pit]) == 6:
                myScore += 1
            # If opponent has potential for extra turn, than subtract 1 from score
            if (pit + board.P2Cups[pit]) == 6:
                oppScore += 1

        return myScore - oppScore

    def alphaBetaMove(self, board, ply, alpha=-INFINITY, beta=INFINITY):
        current_player = self
        if (board.gameOver() or  ply == 0):
            return (current_player.score(board), None)

        if (current_player.num == 1):
            best_move = -1
            maximizer_score = -INFINITY
            for nmove in board.legalMoves(current_player):
                nboard = deepcopy(board)
                nboard.makeMove(current_player, nmove)
                nply = ply - 1
                nplayer = dmd8603(current_player.opp, current_player.type, current_player.ply)
                nscore, retmove = nplayer.alphaBetaMove(nboard, nply, alpha, beta)
                if (nscore > maximizer_score):
                    maximizer_score = nscore
                    best_move = nmove
                alpha = max(alpha, maximizer_score)
                if (beta <= alpha):
                    break
            return maximizer_score, best_move
        if (current_player.num == 2):
            best_move = -1
            minimizer_score = INFINITY
            for nmove in board.legalMoves(current_player):
                nboard = deepcopy(board)
                nboard.makeMove(current_player, nmove)
                nply = ply - 1
                nplayer = dmd8603(current_player.opp, current_player.type, current_player.ply)
                nscore, retmove = nplayer.alphaBetaMove(nboard, nply, alpha, beta)
                if (nscore < minimizer_score):
                    minimizer_score = nscore
                    best_move = nmove
                beta = min(minimizer_score, beta)
                if (beta <= alpha):
                    break
            return minimizer_score, best_move



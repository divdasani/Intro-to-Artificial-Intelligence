from MancalaBoard import *
from dmd8603 import *
from MancalaGUI import *


player1 = dmd8603(1, dmd8603.ABPRUNE,2)
player2 = dmd8603(2, dmd8603.RANDOM,2)
startGame(player1, player2)
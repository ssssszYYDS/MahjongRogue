

import math


from Base import *


class CommonEvent(object):
    def __init__(self, game):
        self.game = game

    def right_hand_in(self, card):
        pass

    def right_hand_out(self, card):
        if card is not None:
            card.back_color = Constants.CARD_LEVEL[card.level]

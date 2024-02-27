

import math


from Base import *


class CommonEvent(object):
    def __init__(self, game):
        self.game = game

    def right_hand_in(self, card):
        if card is not None:
            card.back_color = tuple(min(1, 0.3*(math.sin(2.5*self.game.time)+1)+0.5) *
                                    c for c in Constants.CARD_LEVEL[card.level])
            self.game.ui.cardImages.fill(card.back_color, card.rect)
            x, y = card.rect.topleft
            self.game.ui.cardImages.blit(card.picture, (x+2, y+5))

    def right_hand_out(self, card):
        if card is not None:
            card.back_color = Constants.CARD_LEVEL[card.level]

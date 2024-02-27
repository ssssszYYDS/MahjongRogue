

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

    def vision_update(self):
        if self.game.right_hand is not None:
            self.game.right_hand.back_color = tuple(min(1, 0.3*(math.sin(2.5*self.game.time)+1)+0.5) *
                                                    c for c in Constants.CARD_LEVEL[self.game.right_hand.level])
            self.game.ui.cardImages.fill(self.game.right_hand.back_color, self.game.right_hand.rect)
            x, y = self.game.right_hand.rect.topleft
            self.game.ui.cardImages.blit(self.game.right_hand.picture, (x+2, y+5))

    def end_check(self):
        if len(self.game.deck) == 0:
            self.game.ui.plot()
            self.game.manager.end()
            return True
        return False

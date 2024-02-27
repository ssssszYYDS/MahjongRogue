import os
import pygame as pg


from Base import *


class Loader(object):
    resourcePath = os.path.join(os.path.dirname(__file__), "..", "resources")
    cardsImage = pg.image.load(os.path.join(resourcePath, "cards.png"))
    background = pg.image.load(os.path.join(resourcePath, "background.png"))

    def __init__(self, game):
        self.game = game

    def load_cards(self, card, n):
        width = 195
        height = 255

        source_rect = pg.Rect(Constants.CARD_POSITION[card.cardStr][0],
                              Constants.CARD_POSITION[card.cardStr][1], width, height)
        cardImages = pg.Surface((width, height))
        cardImages.blit(Loader.cardsImage, (0, 0), source_rect)

        scaled_image = pg.transform.scale(cardImages, (self.game.ui.CARD_WIDTH, self.game.ui.CARD_HEIGHT))
        scaled_image.set_colorkey((0, 0, 0))

        rect = self.game.ui.get_hands_rect(n)
        x, y = rect.topleft

        self.game.ui.cardImages.fill(card.back_color, rect)
        self.game.ui.cardImages.blit(scaled_image, (x+2, y+5))

        self.game.manager.common_event.right_hand_out(self.game.right_hand)
        self.game.right_hand = card

        card.picture = scaled_image
        card.rect = rect

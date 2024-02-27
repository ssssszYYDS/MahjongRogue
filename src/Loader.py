import os
import pygame as pg


from Base import *
from UI import UI


class Loader:
    resourcePath = os.path.join(os.path.dirname(__file__), "..", "resources")
    cardsImage = pg.image.load(os.path.join(resourcePath, "cards.png"))
    background = pg.image.load(os.path.join(resourcePath, "background.png"))

    def __init__(self):
        pass

    @staticmethod
    def load_cards(game, card, n):
        width = 195
        height = 255

        source_rect = pg.Rect(Constants.CARD_POSITION[card.cardStr][0],
                              Constants.CARD_POSITION[card.cardStr][1], width, height)
        cardImages = pg.Surface((width, height))
        cardImages.blit(Loader.cardsImage, (0, 0), source_rect)

        scaled_image = pg.transform.scale(cardImages, (UI.CARD_WIDTH, UI.CARD_HEIGHT))
        scaled_image.set_colorkey((0, 0, 0))

        rect = UI.get_hands_rect(n)
        x, y = rect.topleft

        game.ui.cardImages.fill(card.back_color, rect)
        game.ui.cardImages.blit(scaled_image, (x+2, y+5))

        if game.right_first is not None:
            game.right_first.back_color = Constants.CARD_LEVEL[game.right_first.level]
        game.right_first = card

        card.picture = scaled_image
        card.rect = rect

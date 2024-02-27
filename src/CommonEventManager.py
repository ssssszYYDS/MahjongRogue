import pygame as pg
import sys
import math

from Base import *
from Loader import Loader
from UI import UI


class CommonEventManager(object):
    @staticmethod
    def is_in_rect(pos, rect):
        x, y = pos
        rx, ry, rw, rh = rect
        if (rx <= x <= rx+rw) and (ry <= y <= ry+rh):
            return True
        return False

    def __init__(self, game):
        self.game = game
        self.autoSort = False
        self.settingMode = False

    def check_button_down(self, event, button):
        if CommonEventManager.is_in_rect(event.pos, button.button_rect):
            button.button.fill(button.button_click_color)
            button.press_button = True
            button.press()
            return True
        return False

    def check_button_up(self, event, button):
        if CommonEventManager.is_in_rect(event.pos, button.button_rect):
            button.button.fill(button.button_color)
            button.press_button = False
            return True
        return False

    def check_button_over(self, event, button):
        if CommonEventManager.is_in_rect(event.pos, button.button_rect_raw):
            button.button.fill(button.button_hover_color)
            return True
        else:
            button.button.fill(button.button_color)
            return False

    def refresh(self):
        if self.autoSort:
            self.sort_hands(False)
        for i in range(Constants.MAX_HANDS+1):
            self.game.ui.cardImages.fill((0, 0, 0), UI.get_hands_rect(i))
        for i, card in enumerate(self.game.hands):
            card.rect = UI.get_hands_rect(i)
            x, y = card.rect.topleft
            self.game.ui.cardImages.fill(card.back_color, card.rect)
            self.game.ui.cardImages.blit(card.picture, (x+2, y+5))
        for i in range(len(self.game.hands), Constants.MAX_HANDS+1):
            self.game.ui.cardImages.fill((100, 100, 100), UI.get_hands_rect(i))
        self.game.ui.plot()

    def draw(self, n=Constants.MAX_HANDS):
        if len(self.game.deck) == 0:
            return None
        card = self.game.deck.pop(0)
        card.holder = 1
        Loader.load_cards(self.game, card, n)
        print(f"draw {card.cardStr}")
        if self.autoSort:
            self.sort_hands()
        self.game.ui.plot()
        return card

    def drop(self, n):
        if n >= len(self.game.hands):
            return
        card = self.game.hands.pop(n)
        if id(card) == id(self.game.right_first):
            self.game.right_first = None
        self.game.ui.cardImages.fill((0, 0, 0), card.rect)
        card.holder = -1
        card.rect = None
        card.picture = None
        print(f'drop {card.cardStr}')
        if self.autoSort:
            self.refresh()
        self.game.ui.plot()

    def swap(self, a, b):
        if a == b:
            return
        print(f'swap {self.game.hands[b].cardStr} {self.game.hands[a].cardStr}')

        self.game.hands[a].rect, self.game.hands[b].rect = self.game.hands[b].rect, self.game.hands[a].rect

        x, y = self.game.hands[a].rect.topleft
        self.game.ui.cardImages.fill(self.game.hands[a].back_color, self.game.hands[a].rect)
        self.game.ui.cardImages.blit(self.game.hands[a].picture, (x+2, y+5))

        x, y = self.game.hands[b].rect.topleft
        self.game.ui.cardImages.fill(self.game.hands[b].back_color, self.game.hands[b].rect)
        self.game.ui.cardImages.blit(self.game.hands[b].picture, (x+2, y+5))

        self.game.ui.plot()

        self.game.hands[a], self.game.hands[b] = self.game.hands[b], self.game.hands[a]

    def sort_hands(self, refresh=True):
        self.game.hands.sort(key=lambda x: x.cardNum)
        if refresh:
            self.refresh()

    def next_hands(self):
        if len(self.game.hands) < Constants.MAX_HANDS + 1:
            self.game.hands.append(self.draw(len(self.game.hands)))
            self.refresh()
        else:
            print("Please drop a card first!")

    def update(self, time, dt):
        if self.game.right_first is not None:
            self.game.right_first.back_color = tuple(min(1, 0.3*(math.sin(2.5*time)+1)+0.5) *
                                                     c for c in Constants.CARD_LEVEL[self.game.right_first.level])
            self.game.ui.cardImages.fill(self.game.right_first.back_color, self.game.right_first.rect)
            x, y = self.game.right_first.rect.topleft
            self.game.ui.cardImages.blit(self.game.right_first.picture, (x+2, y+5))

    def setting(self):
        self.game.running = False
        self.settingMode = True

        self.game.ui.setting.fill((128, 128, 128), (0, 0, Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
        self.game.screen.blit(self.game.ui.setting, (0, 0))

        self.game.screen.blit(self.game.ui.autoSort_button.button, self.game.ui.autoSort_button.button_rect.topleft)
        self.game.screen.blit(self.game.ui.autoSort_button.button_text, self.game.ui.autoSort_button.button_text_rect)
        self.game.screen.blit(self.game.ui.resume_button.button, self.game.ui.resume_button.button_rect.topleft)
        self.game.screen.blit(self.game.ui.resume_button.button_text, self.game.ui.resume_button.button_text_rect)

        pg.display.update()

        while self.settingMode:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit(0)
                if pg.key.get_pressed()[pg.K_ESCAPE]:
                    self.settingMode = False
                    break

                # 鼠标按下，让状态变成可以移动
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.check_button_down(event, self.game.ui.autoSort_button)
                    self.check_button_down(event, self.game.ui.resume_button)
                    self.game.ui.plot()

                # 鼠标弹起，让状态变成不可以移动
                if event.type == pg.MOUSEBUTTONUP:
                    self.check_button_up(event, self.game.ui.autoSort_button)
                    self.check_button_up(event, self.game.ui.resume_button)
                    self.game.ui.plot()

                # 鼠标移动对应的事件
                if event.type == pg.MOUSEMOTION:
                    pass

                # 鼠标悬停对应的事件
                if event.type == pg.MOUSEMOTION:
                    self.check_button_over(event, self.game.ui.autoSort_button)
                    self.check_button_over(event, self.game.ui.resume_button)
                    self.game.ui.plot()

        self.game.ui.setting.fill((0, 0, 0))
        self.game.ui.plot()

        self.game.running = True

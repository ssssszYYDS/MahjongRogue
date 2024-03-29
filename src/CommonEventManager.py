import pygame as pg
import sys

from Base import *
from Checker import Checker
from CommonEvent import CommonEvent
from Utils import Utils


class CommonEventManager(object):

    def __init__(self, game):
        self.game = game
        self.common_event = CommonEvent(game)
        self.checker = Checker(game)
        self.autoSort = False
        self.settingMode = False

    def check_button_down(self, event, buttons):
        if type(buttons) != list:
            raise ValueError("buttons are not list type!")
        for button in buttons:
            if Utils.is_in_rect(event.pos, button.button_rect):
                button.button.fill(button.button_click_color)
                button.press_button = True
                button.press()

    def check_button_up(self, event, buttons):
        if type(buttons) != list:
            raise ValueError("buttons are not list type!")
        for button in buttons:
            if Utils.is_in_rect(event.pos, button.button_rect):
                button.button.fill(button.button_color)
                button.press_button = False

    def check_button_over(self, event, buttons):
        if type(buttons) != list:
            raise ValueError("buttons are not list type!")
        for button in buttons:
            if Utils.is_in_rect(event.pos, button.button_rect_raw):
                button.button.fill(button.button_hover_color)
            else:
                button.button.fill(button.button_color)

    def refresh(self, sort=True):
        if self.autoSort and sort:
            self.sort_hands(refresh=False)
        self.game.ui.cardImages.fill((0, 0, 0))
        for i, card in enumerate(self.game.hands):
            card.rect = self.game.ui.get_hands_rect(i)
            x, y = card.rect.topleft
            self.game.ui.cardImages.fill(card.back_color, card.rect)
            self.game.ui.cardImages.blit(card.picture, (x+2, y+5))
        for i in range(len(self.game.hands), Constants.MAX_HANDS+1):
            self.game.ui.cardImages.fill((100, 100, 100), self.game.ui.get_hands_rect(i))
        self.game.ui.plot()

    def draw(self, n=Constants.MAX_HANDS):
        if len(self.game.deck) == 0:
            return None
        card = self.game.deck.pop(0)
        card.holder = 1
        self.game.loader.load_cards(card, n)
        print(f"draw {card.cardStr}")
        self.common_event.right_hand_in(self.game.right_hand)
        self.game.ui.plot()
        return card

    def drop(self, n):
        if n >= len(self.game.hands):
            return
        self.game.can_hu = False
        card = self.game.hands.pop(n)
        if id(card) == id(self.game.right_hand):
            self.game.right_hand = None
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
        if self.game.right_hand is not None:
            for i, card in enumerate(self.game. hands):
                if id(card) == id(self.game.right_hand) and i != len(self.game.hands)-1:
                    self.game.hands[i], self.game.hands[-1] = self.game.hands[-1], self.game.hands[i]
                    break
            self.game.hands = sorted(self.game.hands[:-1], key=lambda x: x.cardNum)
            self.game.hands.append(self.game.right_hand)
        else:
            self.game.hands.sort(key=lambda x: x.cardNum)
        if refresh:
            self.refresh(sort=False)

    def next_hands(self):
        if not self.deck_over_check():
            if len(self.game.hands) < Constants.MAX_HANDS + 1:
                self.game.hands.append(self.draw(len(self.game.hands)))
                self.refresh()
                self.hands_hu_check()
            else:
                print("Please drop a card first!")
        print(f"{len(self.game.deck)} cards left in deck.")

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
                    self.check_button_down(event, [self.game.ui.autoSort_button, self.game.ui.resume_button])
                    self.game.ui.plot()

                # 鼠标弹起，让状态变成不可以移动
                if event.type == pg.MOUSEBUTTONUP:
                    self.check_button_up(event, [self.game.ui.autoSort_button, self.game.ui.resume_button])
                    self.game.ui.plot()

                # 鼠标移动对应的事件
                if event.type == pg.MOUSEMOTION:
                    pass

                # 鼠标悬停对应的事件
                if event.type == pg.MOUSEMOTION:
                    self.check_button_over(event, [self.game.ui.autoSort_button, self.game.ui.resume_button])
                    self.game.ui.plot()

            self.game.dt = self.game.clock.tick(Constants.FPS)  # 60 FPS
            self.game.time = pg.time.get_ticks() / 1000

        self.game.ui.setting.fill((0, 0, 0))
        self.game.ui.plot()

        self.game.running = True

    def deck_over_check(self):
        if len(self.game.deck) == 0:
            self.game.ui.plot()
            self.game.end()
            return True
        return False

    def hands_hu_check(self):
        # [[('1m', '1m', '1m'), ('2m', '2m', '2m'), ('3m', '3m', '3m'), ('3z', '3z', '3z'), ('7z', '7z')], [('1m', '2m', '3m'), ('1m', '2m', '3m'), ('1m', '2m', '3m'), ('3z', '3z', '3z'), ('7z', '7z')]]
        hu_cardss = self.checker.check_now()
        if hu_cardss is None or len(hu_cardss) == 0:
            return False
        self.game.can_hu = True
        self.game.hu_cardss = hu_cardss
        print(f"can hu: {hu_cardss}")
        return True

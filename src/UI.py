import pygame as pg

from Base import Constants
from collections import Counter


class UI(object):

    class Button(object):
        def __init__(self, size,  color, hover_color, click_color, text, rect, func):
            self.button = pg.Surface(size)
        # 定义按钮颜色
            self.button_color = color  # 灰色
            self.button_hover_color = hover_color   # 鼠标悬停时的颜色
            self.button_click_color = click_color   # 鼠标点击时的颜色
            self.button.fill(self.button_color)  # 灰色UI

            self.button_rect_raw = rect
            self.button_rect = pg.Rect(self.button_rect_raw)

            self.button_text = text
            self.button_text
            self.button_text_rect = self.button_text.get_rect(center=self.button_rect.center)

            self.func = func    # 按钮功能

        def press(self, *args, **kwargs):
            self.func(*args, **kwargs)

    def __init__(self, game):
        self.CARD_WIDTH = Constants.WINDOW_WIDTH / 18
        self.CARD_HEIGHT = self.CARD_WIDTH / 195 * 255
        self.GAP = Constants.WINDOW_WIDTH / 150
        self.EXT_GAP_RATE = 0.5

        self.game = game
        self.window_w, self.window_h = game.screen.get_size()

        self.background = pg.Surface(game.screen.get_size())
        self.background.fill((0, 128, 0))  # 绿色背景

        self.sort_button = self.Button((self.window_w/30, self.window_h/10), (128, 128, 128), (150, 150, 150), (100, 100, 100),
                                       pg.font.Font(None, 36).render("sort", True, (255, 255, 255)),
                                       (self.window_w*29/30, self.window_h*2/3, self.window_w/30, self.window_h/10),
                                       lambda: game.manager.sort_hands()
                                       )

        self.next_button = self.Button((self.window_w/30, self.window_h/10), (128, 0, 0), (150, 0, 0), (100, 0, 0),
                                       pg.font.Font(None, 36).render("next", True, (255, 255, 255)),
                                       (*self.sort_button.button_rect.bottomleft, self.window_w/30, self.window_h/10),
                                       lambda: game.manager.next_hands()
                                       )

        self.setting_button = self.Button((self.window_w/10, self.window_h/10), (128, 128, 128), (150, 150, 150), (100, 100, 100),
                                          pg.font.Font(None, 36).render("Setting", True, (255, 255, 255)),
                                          (self.window_w*9/10, 0, self.window_w/10, self.window_h/10),
                                          lambda: game.manager.setting()
                                          )

        def autoSort():
            print(f"autoSort: {game.manager.autoSort} -> {not game.manager.autoSort}")
            game.manager.autoSort = not game.manager.autoSort
            self.autoSort_button.button_text = pg.font.Font(None, 36).render("auto sort: on" if game.manager.autoSort else "auto sort: off",
                                                                             True, (1, 1, 1))
            pg.draw.rect(game.screen, (255, 255, 255), self.autoSort_button.button_text_rect)  # 清除旧文本
            game.screen.blit(self.autoSort_button.button_text, self.autoSort_button.button_text_rect)
            pg.display.update()
        self.autoSort_button = self.Button((self.window_w/10, self.window_h/20), (255, 255, 255), (150, 150, 150), (100, 100, 100),
                                           pg.font.Font(None, 36).render("auto sort: off", True, (1, 1, 1)),
                                           (self.window_w*2/10, self.window_h*4/10, self.window_w/10, self.window_h/20),
                                           func=autoSort
                                           )

        def resume():
            game.manager.settingMode = False
            pg.draw.rect(game.screen, (255, 255, 255), self.resume_button.button_rect)
            game.screen.blit(self.resume_button.button_text, self.resume_button.button_text_rect)
            pg.display.update()
        self.resume_button = self.Button((self.window_w/10, self.window_h/20), (255, 255, 255), (150, 150, 150), (100, 100, 100),
                                         pg.font.Font(None, 36).render("continue", True, (1, 1, 1)),
                                         (self.window_w*7/10, self.window_h*4/10, self.window_w/10, self.window_h/20),
                                         func=resume
                                         )

        def click_deck():
            print(f"click deck!")
            pass
        self.deck_button = self.Button((self.window_w/10, self.window_h/10), (0, 0, 128), (0, 0, 150), (0, 0, 100),
                                       pg.font.Font(None, 36).render(f"??? cards", True, (255, 255, 255)),
                                       (self.window_w*9/10, self.window_h*3/10, self.window_w/10, self.window_h/10),
                                       func=click_deck
                                       )

        def click_hu():
            # TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
            # if not game.can_hu:
            #     return
            print(f"click hu!!!")
            self._render_choose_hu_type(self.game.hu_cardss)

        self.hu_button = self.Button((self.window_w/5, self.window_h/10), (128, 0, 0), (150, 0, 0), (100, 0, 0),
                                     pg.font.Font(None, 42).render(f"Hu", True, (255, 165, 0)),
                                     (self.window_w*6/10, self.window_h*5/10, self.window_w/5, self.window_h/10),
                                     func=click_hu
                                     )

        self.cardImages = pg.Surface(game.screen.get_size())
        self.cardImages.set_colorkey((0, 0, 0))

        self.moveCardImages = pg.Surface(game.screen.get_size())
        self.moveCardImages.set_colorkey((0, 0, 0))
        self.moveCardImages.set_alpha(128)

        self.hu_type_choosing_layer = pg.Surface(game.screen.get_size())
        self.hu_type_choosing_layer.set_colorkey((0, 0, 0))
        self.hu_type_choosing_layer.set_alpha(128)

        self.hu_seq_choosing_layer = pg.Surface(game.screen.get_size())
        self.hu_seq_choosing_layer.set_colorkey((0, 0, 0))
        self.hu_seq_choosing_layer.set_alpha(128)

        self.setting = pg.Surface(game.screen.get_size())
        self.setting.set_colorkey((0, 0, 0))

        self.is_move = False
        self.drag_id = -1

    def update_deck_button(self):
        self.deck_button.button_text = pg.font.Font(None, 36).render(
            f"{len(self.game.deck)} cards", True, (255, 255, 255))
        pg.draw.rect(self.game.screen, (0, 0, 128), self.deck_button.button_text_rect)  # 清除旧文本
        self.game.screen.blit(self.deck_button.button_text, self.deck_button.button_text_rect)

    def _render_layer(self, layer):
        self.game.screen.blit(layer, (0, 0))

    def _render_button(self, button):
        self.game.screen.blit(button.button, button.button_rect.topleft)
        self.game.screen.blit(button.button_text, button.button_text_rect)

    def _render_choose_hu_type(self, hu_cardss):

        cards_counter = Counter([hand.cardStr for hand in self.game.hands])
        self._render_choose_hu_seq(cards_counter)

    def _render_choose_hu_seq(self, cards_counter):
        pass

    def plot(self):
        self._render_layer(self.background)

        self._render_button(self.sort_button)
        self._render_button(self.next_button)
        self._render_button(self.setting_button)
        self._render_button(self.deck_button)
        self.update_deck_button()

        if self.game.can_hu:
            self._render_button(self.hu_button)

        self._render_layer(self.cardImages)
        self._render_layer(self.moveCardImages)
        self._render_layer(self.setting)

        if self.game.manager.settingMode:
            self._render_button(self.autoSort_button)
            self._render_button(self.resume_button)

        pg.display.update()

    def get_hands_rect(self, n):
        x = (Constants.WINDOW_WIDTH - (self.CARD_WIDTH+self.GAP) * (Constants.MAX_HANDS + 1 + self.EXT_GAP_RATE)) / 2 + n * (self.CARD_WIDTH+self.GAP) \
            if n != Constants.MAX_HANDS else (Constants.WINDOW_WIDTH - (self.CARD_WIDTH + self.GAP) * (Constants.MAX_HANDS + 1 + self.EXT_GAP_RATE)) / 2 + (n + self.EXT_GAP_RATE) * (self.CARD_WIDTH+self.GAP)
        y = Constants.WINDOW_HEIGHT - self.CARD_HEIGHT
        return pg.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)

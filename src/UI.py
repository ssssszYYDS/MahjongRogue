import pygame as pg

from Base import Constants


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

            self.press_button = False

            self.func = func    # 按钮功能

        def press(self, *args, **kwargs):
            self.func(*args, **kwargs)

    def __init__(self, game):
        self.CARD_WIDTH = Constants.WINDOW_WIDTH / 18
        self.CARD_HEIGHT = self.CARD_WIDTH / 195 * 255
        self.GAP = Constants.WINDOW_WIDTH / 150
        
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

        self.cardImages = pg.Surface(game.screen.get_size())
        self.cardImages.set_colorkey((0, 0, 0))

        self.moveCardImages = pg.Surface(game.screen.get_size())
        self.moveCardImages.set_colorkey((0, 0, 0))
        self.moveCardImages.set_alpha(128)

        self.setting = pg.Surface(game.screen.get_size())
        self.setting.set_colorkey((0, 0, 0))

        self.is_move = False
        self.drag_id = -1

    def plot(self):
        self.game.screen.blit(self.background, (0, 0))

        self.game.screen.blit(self.sort_button.button, self.sort_button.button_rect.topleft)
        self.game.screen.blit(self.sort_button.button_text, self.sort_button.button_text_rect)

        self.game.screen.blit(self.next_button.button, self.next_button.button_rect.topleft)
        self.game.screen.blit(self.next_button.button_text, self.next_button.button_text_rect)

        self.game.screen.blit(self.setting_button.button, self.setting_button.button_rect.topleft)
        self.game.screen.blit(self.setting_button.button_text, self.setting_button.button_text_rect)

        self.game.screen.blit(self.cardImages, (0, 0))
        self.game.screen.blit(self.moveCardImages, (0, 0))
        self.game.screen.blit(self.setting, (0, 0))

        if self.game.manager.settingMode:
            self.game.screen.blit(self.autoSort_button.button, self.autoSort_button.button_rect.topleft)
            self.game.screen.blit(self.autoSort_button.button_text, self.autoSort_button.button_text_rect)

            self.game.screen.blit(self.resume_button.button, self.resume_button.button_rect.topleft)
            self.game.screen.blit(self.resume_button.button_text, self.resume_button.button_text_rect)

        pg.display.update()

    def get_hands_rect(self, n):
        x = (Constants.WINDOW_WIDTH - (self.CARD_WIDTH+self.GAP) * 14.5) / 2 + n * (self.CARD_WIDTH+self.GAP) \
            if n != Constants.MAX_HANDS else (Constants.WINDOW_WIDTH - (self.CARD_WIDTH+self.GAP) * 14.5) / 2 + (n+0.5) * (self.CARD_WIDTH+self.GAP)
        y = Constants.WINDOW_HEIGHT - self.CARD_HEIGHT
        return pg.Rect(x, y, self.CARD_WIDTH, self.CARD_HEIGHT)

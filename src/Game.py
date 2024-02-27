import pygame as pg
import sys
import random

from Base import *
from CommonEventManager import CommonEventManager
from Card import Card
from Loader import Loader
from UI import UI


class Game(object):
    def __init__(self):
        pg.init()
        if not Constants.DEFAULT_SCREEN:
            screen_info = pg.display.Info()
            print(screen_info)
            if Constants.FULL_WINDOW_SCREEN:
                self.screen = pg.display.set_mode((screen_info.current_w, screen_info.current_h))
            elif Constants.FULL_SCREEN:
                self.screen = pg.display.set_mode((screen_info.current_w, screen_info.current_h), pg.FULLSCREEN)
            else:
                raise ValueError("Invalid screen mode")
            Constants.WINDOW_WIDTH = screen_info.current_w
            Constants.WINDOW_HEIGHT = screen_info.current_h
        else:
            self.screen = pg.display.set_mode((Constants.WINDOW_WIDTH, Constants.WINDOW_HEIGHT))
        pg.display.set_caption('Mahjong Rogue')
        self.clock = pg.time.Clock()
        self.running = False

        self.ui = UI(self)
        self.loader = Loader(self)
        self.manager = CommonEventManager(self)

    def init_game(self):
        self.dt = self.clock.tick(Constants.FPS)  # 60 FPS
        self.time = pg.time.get_ticks() / 1000

        self.all_deck = [Card(cardStr) for cardStr in Constants.ALLCARD]
        self.deck = self.all_deck.copy()
        random.shuffle(self.deck)
        self.hands = []
        self.right_hand = None

        for i in range(Constants.MAX_HANDS):
            self.hands.append(self.manager.draw(i))

        pg.display.update()

    def run(self):
        self.init_game()
        self.running = True
        while self.running:
            if len(self.hands) < Constants.MAX_HANDS + 1:
                self.ui.next_button.press()

            for event in pg.event.get():
                if event.type == pg.QUIT or pg.key.get_pressed()[pg.K_ESCAPE]:
                    self.running = False
                    break
                mouse_buttons = pg.mouse.get_pressed()
                # 鼠标按下，让状态变成可以移动
                if event.type == pg.MOUSEBUTTONDOWN:
                    if mouse_buttons[0]:  # 左键
                        for i, card in enumerate(self.hands):
                            image_x, image_y = card.rect.topleft
                            w, h = card.picture.get_size()

                            if CommonEventManager.is_in_rect(event.pos, (image_x, image_y, w, h)):
                                self.ui.is_move = True
                                self.ui.drag_id = i
                                break
                    elif mouse_buttons[2]:  # 右键
                        for i, card in enumerate(self.hands):
                            image_x, image_y = card.rect.topleft
                            w, h = card.picture.get_size()

                            if CommonEventManager.is_in_rect(event.pos, (image_x, image_y, w, h)):
                                self.manager.drop(i)
                                break

                    self.manager.check_button_down(event, self.ui.sort_button)
                    self.manager.check_button_down(event, self.ui.next_button)
                    self.manager.check_button_down(event, self.ui.setting_button)
                    self.ui.plot()

                # 鼠标弹起，让状态变成不可以移动
                if event.type == pg.MOUSEBUTTONUP:
                    self.ui.moveCardImages.fill((0, 0, 0))
                    for i, card in enumerate(self.hands):
                        image_x, image_y = card.rect.topleft
                        w, h = card.picture.get_size()
                        if CommonEventManager.is_in_rect(event.pos, (image_x, image_y, w, h)):
                            self.manager.swap(i, self.ui.drag_id)
                            self.ui.moveCardImages.fill((0, 0, 0))
                            break
                    else:
                        self.ui.moveCardImages.fill((0, 0, 0))
                        if self.ui.drag_id != -1 and event.pos[1] < Constants.WINDOW_HEIGHT - self.ui.CARD_HEIGHT:
                            self.manager.drop(self.ui.drag_id)

                    self.manager.check_button_up(event, self.ui.sort_button)
                    self.manager.check_button_up(event, self.ui.next_button)
                    self.manager.check_button_up(event, self.ui.setting_button)

                    self.ui.is_move = False
                    self.ui.drag_id = -1
                    self.ui.plot()

                # 鼠标移动对应的事件
                if event.type == pg.MOUSEMOTION:
                    if mouse_buttons[0] and self.ui.is_move:
                        x, y = event.pos
                        color = self.hands[self.ui.drag_id].back_color
                        image = self.hands[self.ui.drag_id].picture
                        image_w, image_h = image.get_size()
                        # 保证鼠标在图片的中心
                        image_y = y-image_h/2
                        image_x = x-image_w/2
                        rect = self.hands[self.ui.drag_id].rect
                        self.ui.moveCardImages.fill((0, 0, 0))
                        self.ui.moveCardImages.fill(color, (image_x, image_y, rect.width, rect.height))
                        self.ui.moveCardImages.blit(image, (image_x+2, image_y+5))
                        self.ui.plot()

                # 鼠标悬停对应的事件
                if event.type == pg.MOUSEMOTION:
                    self.manager.check_button_over(event, self.ui.sort_button)
                    self.manager.check_button_over(event, self.ui.next_button)
                    self.manager.check_button_over(event, self.ui.setting_button)
                    self.ui.plot()

            self.dt = self.clock.tick(Constants.FPS)  # 60 FPS
            self.time = pg.time.get_ticks() / 1000

            self.manager.update()

            # break
            self.ui.plot()
        pg.quit()
        sys.exit(0)


if __name__ == '__main__':
    random.seed(0)
    game = Game()
    game.run()

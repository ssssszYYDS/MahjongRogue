"""__author__ = 余婷"""
# 要求：先在屏幕上显示一张图片，鼠标按下移动的时候，拽着图片跟着一起动。鼠标弹起就不动了
import pygame
import os


# 写一个函数，判断一个点是否在某个范围内
# 点（x,y）
# 范围 rect(x,y,w,h)
def is_in_rect(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx+rw) and (ry <= y <= ry+rh):
        return True
    return False


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((2000, 1000))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('图片拖拽')

    # 显示一张图片
    image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "resources", "cards.png"))
    image_x = 100
    image_y = 100
    screen.blit(image, (image_x, image_y))
    pygame.display.flip()

    # 用来存储图片是否可以移动
    is_move = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            # 鼠标按下，让状态变成可以移动
            if event.type == pygame.MOUSEBUTTONDOWN:
                w, h = image.get_size()
                if is_in_rect(event.pos, (image_x, image_y, w, h)):
                    is_move = True

            # 鼠标弹起，让状态变成不可以移动
            if event.type == pygame.MOUSEBUTTONUP:
                is_move = False

            # 鼠标移动对应的事件
            if event.type == pygame.MOUSEMOTION:
                if is_move:
                    screen.fill((0, 0, 0))
                    x, y = event.pos
                    image_w, image_h = image.get_size()
                    # 保证鼠标在图片的中心
                    image_y = y-image_h/2
                    image_x = x-image_w/2
                    screen.blit(image, (image_x, image_y))
                    pygame.display.update()

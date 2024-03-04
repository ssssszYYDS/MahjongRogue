import re


class Utils:
    @staticmethod
    def is_in_rect(pos, rect):
        x, y = pos
        rx, ry, rw, rh = rect
        if (rx <= x <= rx+rw) and (ry <= y <= ry+rh):
            return True
        return False
    
    @staticmethod
    def cardsStr_2_str(cardsStr):
        s = ''
        # cardsStr ~ [('1m', '1m', '1m'), ('2m', '2m', '2m'), ('3m', '3m', '3m'), ('3z', '3z', '3z'), ('7z', '7z')]
        for mianZi in cardsStr:
            for card in mianZi:
                s += card[0]
            # ['111m', '222m', '333m', '333z', '77z']
            s += mianZi[0][1]
        return ''.join(s) # '111m222m333m333z77z'

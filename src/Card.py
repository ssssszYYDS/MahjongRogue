from enum import Enum

from Base import *
from Loader import Loader


class CardType(Enum):
    MAN = 0
    PIN = 1
    SOU = 2
    ZI = 3

    @classmethod
    def is_hand(cls, type):
        return type.value <= 3


class Card:
    def __init__(self, cardStr=None):
        self.cardType = None
        self.cardNum = None
        self.cardStr = cardStr

        # 自摸时，在手牌中时，自己打出时，对方打出时，吃碰杠时，特殊
        self.effects = [None, None, None, None, None, None]
        self.level = 'white'  # white, green, blue, purple, yellow, red
        self.back_color = Constants.CARD_LEVEL[self.level]

        self.text = None

        self.picture = None
        self.rect = None

        # 0: 牌堆, 1: 手牌, -1: 自己的弃牌, -2: 对方的弃牌, -3: 其他
        self.holder = 0

        if self.cardStr is not None:
            self.cardType = self.get_card_type()
            self.cardNum = self.get_card_num()

            self.text = self.get_card_text()
        else:
            print("Warning: Card is not fully implemented.")

    def get_card_type(self):
        if self.cardStr in Constants.ALLCARD:
            if self.cardStr[1] == 'm':
                return CardType.MAN
            elif self.cardStr[1] == 'p':
                return CardType.PIN
            elif self.cardStr[1] == 's':
                return CardType.SOU
            elif self.cardStr[1] == 'z':
                return CardType.ZI

    def get_card_num(self):
        if CardType.is_hand(self.cardType):
            return int(self.cardStr[0]) + 10 * self.cardType.value

    def get_card_text(self):
        if CardType.is_hand(self.cardType):
            return self.cardStr

    def __str__(self):
        if self.cardType is None:
            raise ValueError("cardType must be not None")
        if CardType.is_hand(self.cardType):
            return f"Card({self.cardStr}) ({self.cardType}) ({self.cardNum})"
        else:
            return f"Card({self.cardType}) ({self.text})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return self.cardNum < other.cardNum

    def __eq__(self, other):
        return self.id() == other.id()

    def __gt__(self, other):
        return self.cardNum > other.cardNum


if __name__ == '__main__':
    # d = {}
    # for card in Constants.ALLCARD:
    #     c = Card(card)
    #     d[card] = c.pos
    # print(d)

    pass

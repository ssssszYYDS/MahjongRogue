import re
from collections import Counter

from Base import *


class Checker(object):
    def __init__(self, game=None):
        self.game = game
        self.cards = []
        self.finalCards = []
        self.tempCards = []
        self.__finalCardsStrSet = set()

    def check_now(self):
        self.cards = self.hands_2_cards(self.sorted_hands(self.game.hands))
        self.finalCards = []

        if self.cards is not None and self.is_valid_cards(self.cards):
            if self.check_hu(self.cards):
                return self.finalCards
            else:
                return None
        else:
            print("手牌数量不为14张或手牌格式错误")

    def check_cards(self, hands):
        if type(hands[0]) == str:
            self.cards = sorted(hands)
        else:
            self.cards = self.hands_2_cards(self.sorted_hands(hands))
        self.finalCards = []

        if self.cards is not None and self.is_valid_cards(self.cards):
            if self.check_hu(self.cards):
                return self.finalCards
            else:
                return None
        else:
            print("手牌数量不为14张或手牌格式错误")

    def is_valid_cards(self, cards):
        # 检查手牌数量是否为 14 张
        if len(cards) != 14:
            print(f"手牌数量={len(cards)}，不为14张")
            return False

        # # 检查手牌格式
        # for card in cards:
        #     if not re.fullmatch(r'(\d+[mps]|[1-7]+z)+', card):
        #         print(f"手牌格式错误：{card}")
        #         return False

        # # 检查每张牌的数量是否小于等于 4 张
        # counts = Counter(cards)
        # for name, count in counts.items():
        #     if count > 4:
        #         print(f"{name}的数量为{count}，大于4张")
        #         return False

        return True

    def regular_recursion_check(self, counts):
        # 如果所有牌都被移除完，则满足和牌条件
        if len(self.tempCards) == 5:
            self.finalCards.append(sorted(self.tempCards.copy()))
            # 移除重复的和牌
            s = ''
            # self.finalCards[-1] = [('1m', '1m', '1m'), ('2m', '2m', '2m'), ('3m', '3m', '3m'), ('3z', '3z', '3z'), ('7z', '7z')]
            for mianZi in self.finalCards[-1]:
                for card in mianZi:
                    s += card[0]
                # ['111m', '222m', '333m', '333z', '77z']
                s += mianZi[0][1]
            s = ''.join(s)
            # ['111m222m333m333z77z']
            if s in self.__finalCardsStrSet:
                self.finalCards.pop()
                return False
            else:
                self.__finalCardsStrSet.add(s)

            return True

        flag = False

        # 遍历所有牌型
        for tile, _ in counts.items():
            num, type = int(tile[0]), tile[1]
            # 如果当前牌的数量大于等于 3，则可以尝试组成顺子或刻子
            if counts[tile] >= 3:
                counts[tile] -= 3
                self.tempCards.append((tile, tile, tile))
                if self.regular_recursion_check(counts):
                    flag = True
                self.tempCards.pop()
                counts[tile] += 3

            if type != 'z' and counts[tile] and counts.get(f"{num+1}{type}") and counts.get(f"{num+2}{type}"):
                counts[tile] -= 1
                counts[f"{num+1}{type}"] -= 1
                counts[f"{num+2}{type}"] -= 1
                self.tempCards.append(
                    (tile, f"{num+1}{type}", f"{num+2}{type}"))
                if self.regular_recursion_check(counts):
                    flag = True
                self.tempCards.pop()
                counts[tile] += 1
                counts[f"{num+1}{type}"] += 1
                counts[f"{num+2}{type}"] += 1

        return flag

    def check_regular(self, cards):
        counts = Counter(cards)

        flag = False
        # 逐个移除雀头，并判断是否满足和牌条件
        for tile in counts:
            if counts[tile] < 2:
                continue

            counts[tile] -= 2
            self.tempCards.append((tile, tile))
            # 检查是否有四组顺子或刻子
            if self.regular_recursion_check(counts):
                flag = True
            self.tempCards.pop()
            counts[tile] += 2

        return flag

    def check_seven_pairs(self, cards):
        if not self.is_valid_cards(cards):
            return False

        counts = Counter(cards)

        for tile in counts:
            if counts[tile] != 2:
                self.tempCards = []
                return False
            else:
                self.tempCards.append((tile, tile))

        self.finalCards.append(self.tempCards)

        return True

    def check_thirteen_orphans(self, cards):
        if not self.is_valid_cards(cards):
            return False

        for orphan in Constants.ORPHANS:
            if orphan not in cards:
                return False

        for tile in cards:
            if tile not in Constants.ORPHANS:
                return False

        self.finalCards.append(tuple(cards))
        return True

    def check_hu(self, cards):
        if self.check_seven_pairs(cards) or self.check_thirteen_orphans(cards) or self.check_regular(cards):
            return True
        return False

    def __repr__(self) -> str:
        return f"Check(\n" + \
            f"cards={self.cards},\n" + \
            f"__finalCardsStrSet={self.__finalCardsStrSet},\n" + \
            f"finalCards={self.finalCards},\n" + \
            f"score={self.score}\n" + \
            f")"

    def sorted_hands(self, hands):
        return sorted(hands, key=lambda x: x.cardNum)

    def hands_2_cards(self, hands):
        return [hand.cardStr for hand in hands]


if __name__ == "__main__":
    checker = Checker()
    # 测试代码
    cards1 = ['1m', '1m', '1m', '4m', '5m', '6m', '7m',
              '8m', '9m', '1z', '2z', '1p', '1p', '3z']  # 非和牌
    print(checker.check_cards(cards1))

    cards2 = ['1m', '9m', '1p', '9p', '1s', '9s', '1m',
              '1z', '2z', '3z', '4z', '5z', '6z', '7z']  # 国士无双
    print(checker.check_cards(cards2))

    cards3 = ['1m', '1m', '2m', '2m', '3m', '3m', '4m', '4m',
              '5m', '5m', '6m', '6m', '7m', '7m']  # 七对子
    print(checker.check_cards(cards3))

    cards4 = ['1m', '2m', '3m', '4m', '5m', '6m', '7m',
              '8m', '9m', '1p', '1p', '1p', '1s', '1s']  # 一般和牌
    print(checker.check_cards(cards4))

    cards5 = ['1m', '1m', '1m', '2m', '2m', '2m', '3m',
              '3m', '3m', '3z', '3z', '3z', '7z', '7z']  # 多种一般和牌
    print(checker.check_cards(cards5))

    cards5 = ['1m', '1m', '1m', '2m', '2m', '2m', '3m',
              '3m', '3m', '4m', '4m', '4m', '1m', '1m']  # 多种一般和牌
    print(checker.check_cards(cards5))

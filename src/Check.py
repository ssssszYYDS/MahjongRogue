import re
from collections import Counter

from Base import *
from Score import Score


class Check:
    def __init__(self, cards=None):
        self.cards = cards
        self.finalCards = []
        self.finalCardsStr = []
        self.score = None
        self.tempCards = []

        if self.cards is not None and self.is_valid_cards(self.cards):
            self.cards = sort_strList(cards)
            self.score = self.get_base_score(self.cards)

    def check(self):
        self.finalCards = []

        if self.cards is not None and self.is_valid_cards(self.cards):
            self.score = self.get_base_score(self.cards)
            if self.finalCards:
                return self.finalCards
            else:
                return None
        else:
            print("手牌数量不为14张或手牌格式错误")

    def check(self, cards):
        self.cards = sort_strList(cards)
        self.finalCards = []
        self.score = None

        if self.cards is not None and self.is_valid_cards(self.cards):
            self.score = self.get_base_score(self.cards)
            if self.finalCards:
                return self.finalCards
            else:
                return None
        else:
            return None

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
            s = ''
            # self.finalCards[-1] = [('1m', '1m', '1m'), ('2m', '2m', '2m'), ('3m', '3m', '3m'), ('3z', '3z', '3z'), ('7z', '7z')]
            for mianZi in self.finalCards[-1]:
                for card in mianZi:
                    s += card[0]
                # ['111m', '222m', '333m', '333z', '77z']
                s += mianZi[0][1]

            # ['111m222m333m333z77z']
            self.finalCardsStr.append(''.join(s))

            for s in self.finalCardsStr[:-1]:
                if self.finalCardsStr[-1] == s:
                    self.finalCardsStr.pop()
                    self.finalCards.pop()
                    return False
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

    def get_regular_score(self, cards):
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

        return Constants.REGULAR_BASE_SCORE if flag else 0

    def get_seven_pairs_score(self, cards):
        if not self.is_valid_cards(cards):
            return 0

        counts = Counter(cards)

        for tile in counts:
            if counts[tile] != 2:
                self.tempCards = []
                return 0
            else:
                self.tempCards.append((tile, tile))

        self.finalCards.append(self.tempCards)

        return Constants.SEVEN_PAIRS_BASE_SCORE

    def get_thirteen_orphans_score(self, cards):
        if not self.is_valid_cards(cards):
            return 0

        for orphan in Constants.ORPHANS:
            if orphan not in cards:
                return 0

        for tile in cards:
            if tile not in Constants.ORPHANS:
                return 0

        self.finalCards.append(tuple(cards))
        return Constants.THIRTEEN_ORPHANS_BASE_SCORE

    def get_base_score(self, cards):
        score = self.get_seven_pairs_score(cards)
        if score:
            return score

        score = self.get_regular_score(cards)
        if score:
            return score

        score = self.get_thirteen_orphans_score(cards)
        if score:
            return score

        return Constants.FAIL_BASE_SCORE

    def __repr__(self) -> str:
        return f"Check(\n" + \
            f"cards={self.cards},\n" + \
            f"finalCardsStr={self.finalCardsStr},\n" + \
            f"finalCards={self.finalCards},\n" + \
            f"score={self.score}\n" + \
            f")"


def sort_strList(cards_strList):
    return sorted(cards_strList, key=lambda x: ord(x[-1])*10+ord(x[0]))


if __name__ == "__main__":
    checker = Check()
    # 测试代码
    cards1 = ['1m', '1m', '1m', '4m', '5m', '6m', '7m',
              '8m', '9m', '1z', '2z', '1p', '1p', '3z']  # 非和牌
    print(Check(cards1))

    cards2 = ['1m', '9m', '1p', '9p', '1s', '9s', '1m',
              '1z', '2z', '3z', '4z', '5z', '6z', '7z']  # 国士无双
    print(Check(cards2))

    cards3 = ['1m', '1m', '2m', '2m', '3m', '3m', '4m', '4m',
              '5m', '5m', '6m', '6m', '7m', '7m']  # 七对子
    print(Check(cards3))

    cards4 = ['1m', '2m', '3m', '4m', '5m', '6m', '7m',
              '8m', '9m', '1p', '1p', '1p', '1s', '1s']  # 一般和牌
    print(Check(cards=cards4))

    cards5 = ['1m', '1m', '1m', '2m', '2m', '2m', '3m',
              '3m', '3m', '3z', '3z', '3z', '7z', '7z']  # 多种一般和牌
    print(Check(cards5))

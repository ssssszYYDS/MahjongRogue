from Base import *


class Score(object):
    def __init__(self, finalCards=None, win=False):
        self.score = 0
        self.baseScore = 0
        self.fuPoints = 20
        self.hanPoints = 0
        self.finalCards = finalCards

    def add_score(self, score):
        self.score += score

    def get_score(self):
        if len(self.finalCards) == 0:  # 未和牌
            self.fuPoints = 0
            return Constants.FAIL_BASE_SCORE
        elif len(self.finalCards) == 1:  # 国士无双
            self.baseScore = Constants.THIRTEEN_ORPHANS_BASE_SCORE
            self.score = Constants.THIRTEEN_ORPHANS_BASE_SCORE
            return self.score
        elif len(self.finalCards) == 7:  # 七对子
            self.baseScore = Constants.SEVEN_PAIRS_BASE_SCORE
            self.fuPoints = 25
            self.hanPoints += 2
        elif len(self.finalCards) == 5:  # 一般和牌
            for mainZi in self.finalCards:
                if len(mainZi) == 2 and mainZi[0][1] == 'z':  # 雀头
                    self.fuPoints += 4
                elif len(mainZi) == 3 and mainZi[0][0] == mainZi[1][0]:  # 刻子
                    if mainZi[0][0] in Constants.THIRTEEN_ORPHANS:
                        self.fuPoints += 8
                    else:
                        self.fuPoints += 4
                elif len(mainZi) == 4:  # 杠子
                    if mainZi[0][0] in Constants.THIRTEEN_ORPHANS:
                        self.fuPoints += 32
                    else:
                        self.fuPoints += 16
                else:  # 顺子
                    self.fuPoints += 2

        self.fuPoints = self.fuPoints // 10 * 10 + (10 if self.fuPoints % 10 else 0)

        if self.hanPoints >= 13:
            return 32000
        elif self.hanPoints >= 11:
            return 24000
        elif self.hanPoints >= 8:
            return 16000
        elif self.hanPoints >= 6:
            return 12000
        elif self.hanPoints >= 5:
            return 8000
        else:
            self.score = (self.baseScore + self.fuPoints * 10) * (2 ** (self.hanPoints - 1))
            return self.score // 100 * 100 + (100 if self.score % 100 else 0)

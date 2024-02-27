class Localization:
    def __init__(self):
        self.language = "zh_CN"
        self.loadLanguage(self.language)

    def loadLanguage(self, language):
        if language == "zh_CN":
            self.language = "zh_CN"
            self.languageDict = {
                "handCardError": "手牌数量不为14张或手牌格式错误",
                "handCardCountError": "手牌数量={0}，不为14张",
                "handCardFormatError": "手牌格式错误：{0}",
                "handCardCountError": "{0}的数量为{1}，大于4张",
            }

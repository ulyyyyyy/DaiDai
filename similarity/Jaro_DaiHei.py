# Copyright (c) 2021 heihei & daidai

from similarity.method.string_distance import NormalizedStringDistance
from similarity.method.string_similarity import NormalizedStringSimilarity


class JaroDaiHei(NormalizedStringSimilarity, NormalizedStringDistance):
    """
    本文实现了 JaroWinkler 算法，为Jaro算法的改进版。
    算法在基于 Jaro 算法基础上给予了起始部分就相同的字符串更高的分数
    计算方法:  dw =  dj + L * P ( 1 + dj)
    其中:
        dw: 最后得分
        dj: Jaro算法得分
        L: 前缀部分匹配的长度
        P: 范围因子常量，用来调整前缀匹配的权值，通常设为 0.1
    """

    def __init__(self, threshold=0.7):
        """
        初始化类
        :param threshold: 阈值t
        """
        self.threshold = threshold  # 阈值t
        self.three = 3
        self.jw_coef = 0.1  # 范围因子常量，通常设为0.1，这里设置成动态  min(0.1, 1.0/len(max_str))

    def get_threshold(self):
        """
        得到阈值
        :return:
        """
        return self.threshold

    def similarity(self, s0, s1):
        """
        计算两个短文本相似度
        当起始部分匹配时返回JaroWinkler算法得分
        当不匹配返回Jaro算法得分
        :param s0: 短文本1
        :param s1: 短文本2
        :return: 计算得分
        """
        if s0 is None:
            raise TypeError("Argument s0 is NoneType.")
        if s1 is None:
            raise TypeError("Argument s1 is NoneType.")
        if s0 == s1:
            return 1.0
        mtp = self.matches(s0, s1)
        m = mtp[0]
        if m == 0:
            return 0.0
        j = (m / len(s0) + m / len(s1) + (m - mtp[1]) / m) / self.three
        # 匹配前缀
        jw = j + min(self.jw_coef, 1.0 / mtp[4]) * mtp[2] * (1 - j)
        # 匹配后缀
        jw = jw - min(self.jw_coef, 1.0 / mtp[4]) * mtp[3] * (1 - jw)
        return jw

    @staticmethod
    def matches(s0, s1):
        """
        对字符串数据进行处理，得到我们需要计算的关键数据列表
        :param s0: 短文本1
        :param s1: 短文本2
        :return: List<int> 包含5个元素：
            matches: 匹配字符数m
            换位字符数t
            prefix: 起始部分匹配字符串数量L
            suffix: 末尾部分匹配字符串数量S
            len(max_str):最长字符串长度
        """
        if len(s0) > len(s1):
            max_str = s0
            min_str = s1
        else:
            max_str = s1
            min_str = s0
        ran = int(max(len(max_str) / 2 - 1, 0))
        match_indexes = [-1] * len(min_str)
        match_flags = [False] * len(max_str)
        matches = 0  # 匹配字符串数量m
        for mi in range(len(min_str)):
            c1 = min_str[mi]
            for xi in range(max(mi - ran, 0), min(mi + ran + 1, len(max_str))):
                if not match_flags[xi] and c1 == max_str[xi]:
                    match_indexes[mi] = xi
                    match_flags[xi] = True
                    matches += 1
                    break

        ms0, ms1 = [0] * matches, [0] * matches
        si = 0
        for i in range(len(min_str)):
            if match_indexes[i] != -1:
                ms0[si] = min_str[i]
                si += 1
        si = 0
        for j in range(len(max_str)):
            if match_flags[j]:
                ms1[si] = max_str[j]
                si += 1
        transpositions = 0  # 偏移量
        for mi in range(len(ms0)):
            if ms0[mi] != ms1[mi]:
                transpositions += 1

        prefix = 0  # 起始部分匹配字符串数量L
        for mi in range(len(min_str)):
            if s0[mi] == s1[mi]:
                prefix += 1
            else:
                break

        suffix = 0
        for sx in range(len(min_str)-1, -1, -1):
            if s0[sx] == s1[sx]:
                suffix += 1
            else:
                break

        return [matches, int(transpositions / 2), prefix, suffix, len(max_str)]


if __name__ == '__main__':
    jaro = JaroDaiHei()
    b = jaro.similarity("数据分析", "数据官")
    print(b)
# 0.7777777777777778

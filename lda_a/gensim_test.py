import gensim
import xlrd
import re
import jieba
from similarity.Jaro_git import JaroWinkler
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pyLDAvis

jaro = JaroWinkler(0)


def remove_punctuation(line):
    line = str(line)
    if line.strip() == '':
        return ''
    rule = re.compile(u"[^\u4E00-\u9FA5]")
    line = rule.sub('', line)
    return line


# 停用词列表
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords


def clean_text(text):
    # 加载停用词
    stopwords = stopwordslist("./baidu_stopwords.txt")
    wordlist = jieba.lcut(text)  # 去除停用词和长度小于2的词语
    wordlist = [w for w in wordlist if w not in stopwords and len(w) > 2]  # 将中文数据组织成类似西方于洋那样，词语之间以空格间隔
    document = " ".join(wordlist)
    return document


def get_corpus():
    allowed_list = ["管培生", "数据员", "高数老师", "生管", "人力字段", "业务员", "人事劳资", "统计师", "用户研究", "管理类", "财务管理", "助理买手", "软件测试",
                    "销售员", "会计"]
    corpus = []
    df = pd.read_excel(r"./../similarity/data.xls", sheet_name=3)
    df['工作名称'] = df['工作名称'].str.replace("[^\u4e00-\u9fa5]", "")
    df['职位描述'] = df['职位描述'].str.replace("[^\u4e00-\u9fa5]", "")
    for i in range(len(list(df['工作名称']))):
        for ele in allowed_list:
            if jaro.similarity(list(df['工作名称'])[i], ele) > 0.7:
                corpus.append(list(df['职位描述'])[i])
    return corpus


def corpus_similarity(corpus: list):
    pass


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("主题 {} : {}".format(topic_idx,
                                  "|".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])))


if __name__ == '__main__':
    text_data = get_corpus()
    corpus = []
    stopwords = stopwordslist("./baidu_stopwords.txt")
    for data in text_data:
        b = "  ".join(w for w in list(jieba.cut(data)) if w not in stopwords)
        corpus.append(b)

    # no_features = 1000
    #
    tfidf = TfidfVectorizer()
    tfidf_features = tfidf.fit_transform(corpus)
    tfidf_feature_names = tfidf.get_feature_names()

    nmf_tfidf = NMF(n_components=15, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf_features)
    no_top_words = 10
    print('---------------NMF-tfidf_features 主题-----------------------------------------')
    display_topics(nmf_tfidf, tfidf_feature_names, no_top_words)

    # LDA
    lda_cv = LatentDirichletAllocation(n_components=15, max_iter=50, learning_method='online', learning_offset=50.,
                                       random_state=0).fit(tfidf_features)

    print('--------------Lda-tfidf_features 主题--------------------------------')
    display_topics(lda_cv, tfidf_feature_names, no_top_words)

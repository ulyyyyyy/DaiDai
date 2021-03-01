import gensim
import xlrd
import re
import jieba
from gensim.corpora import dictionary


# 定义删除除字母,数字，汉字以外的所有符号的函数
from sklearn.decomposition import LatentDirichletAllocation, NMF
from sklearn.feature_extraction.text import TfidfVectorizer


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


# 加载停用词
stopwords = stopwordslist("./baidu_stopwords.txt")


def get_corpus():
    xls = xlrd.open_workbook_xls("./../data.xls", encoding_override="utf-8")
    sheet = xls.sheet_by_index(0)
    ret_corpus = []
    job_desc_list = sheet.col_values(11, start_rowx=1)
    for desc in job_desc_list:
        desc = remove_punctuation(desc)
        ret_corpus.append(desc)
    return ret_corpus


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("主题 {} : {}".format(topic_idx,
                                  "|".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])))



if __name__ == '__main__':
    text_data = get_corpus()
    corpus = []
    for data in text_data:
        b = "  ".join(w for w in list(jieba.cut(data)) if w not in stopwords)
        corpus.append(b)

    # corpus = [dictionary.doc2bow(corpu) for corpu in corpus]
    no_features = 1000

    tfidf = TfidfVectorizer(max_features=no_features)
    tfidf_features = tfidf.fit_transform(corpus)
    tfidf_feature_names = tfidf.get_feature_names()

    nmf_tfidf = NMF(n_components=15, random_state=1, alpha=.1, l1_ratio=.5, init='nndsvd').fit(tfidf_features)
    no_top_words = 10
    print('---------------NMF-tfidf_features 主题-----------------------------------------')
    display_topics(nmf_tfidf, tfidf_feature_names, no_top_words)

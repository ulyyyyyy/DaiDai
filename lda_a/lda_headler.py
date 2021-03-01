import lda as lda
import xlrd
import re
from sklearn.feature_extraction.text import CountVectorizer

import numpy as np
re_job_desc = re.compile("[职责|要求]+[：]*(.*)[^\r\n]*")


def get_corpus():
    xls = xlrd.open_workbook_xls("./../data.xls", encoding_override="utf-8")
    sheet = xls.sheet_by_index(0)
    job_desc_list = sheet.col_values(11, start_rowx=1)
    corpus = []

    for desc in job_desc_list:
        d = re.findall(re_job_desc, desc)
        d_str = d[0]
        corpus.append(d_str)
    return corpus


if __name__ == '__main__':
    corpus = get_corpus()
    # print(corpus)
    # tokens = []
    #
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus)
    vocab = vectorizer.get_feature_names()
    analyze = vectorizer.build_analyzer()
    weight = X.toarray()  # 得到文档-单词的矩阵
    #
    model = lda.LDA(n_topics=15, n_iter=100, random_state=1)
    model.fit((100 * np.asarray(weight)).astype(int))  # lda迭代训练之后，得到主题-单词分布，以及文档-主题的分布
    topic_words = model.topic_word_  # 主题-单词的分布情况
    doc_topic = model.doc_topic_  # 文档-主题的分布情况
    #
    for i, topic_dist in enumerate(topic_words):
        topic_word_pr = np.array(vocab)[np.argsort(topic_dist)][:-6:-1]
        print('TOPIC:{}\n{}'.format(i + 1, ' '.join(topic_word_pr)))
    label = []
    for n in range(10):
        topic_most_pr = doc_topic[n].argmax()
        label.append(topic_most_pr)
        print("doc:{},topic:{}".format(n, topic_most_pr))
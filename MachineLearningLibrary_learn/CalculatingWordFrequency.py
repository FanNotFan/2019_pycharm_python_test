from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

corpus = ["我 来到 北京 清华大学",
          "他 来到 了 网易 杭研 大厦",
          "小明 硕士 毕业 与 中国 科学院",
          "我 爱 北京 天安门"]

# CountVectorizer是一个向量计数器
# 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
vectorizer = CountVectorizer()

# token_pattern指定统计词频的模式, 不指定, 默认如英文, 不统计单字
# vectorizer = CountVectorizer(token_pattern='\\b\\w+\\b')

# 这说明fit_transform把corpus二维数组转成了一个csr_matrix类型（稀疏矩阵）
print("类型：\n", type(vectorizer.fit_transform(corpus)))

# 这就是稀疏矩阵的表示形式，即把二维数组里的所有词语组成的稀疏矩阵的第几行第几列有值
csr_matrix = vectorizer.fit_transform(corpus)
print("稀疏矩阵：\n", csr_matrix)

# 把稀疏矩阵输出成真实矩阵
actual_matrix_result = vectorizer.fit_transform(corpus).todense()
print("稀疏矩阵输出成真实矩阵: \n", actual_matrix_result)

# 该类会统计每个词语的tf-idf权值
transformer = TfidfTransformer()
# 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
# tfidf = transformer.fit_transform(csr_matrix)

# 获取词袋模型中的所有词语
word = vectorizer.get_feature_names()
# 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
weight = tfidf.toarray()

for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    for j in range(len(word)):
        print(word[j], weight[i][j])

print("类型：\n", type(tfidf))

# tf-idf数据
print("tfidf:\n", tfidf)

print("tfidf.todense:\n", tfidf.todense())

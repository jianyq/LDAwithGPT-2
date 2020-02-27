from gensim import corpora, models, similarities
from mpl_toolkits.mplot3d import Axes3D
from lxml import etree
import matplotlib.pyplot as plt
import numpy as np
import gensim
import jieba
import re
train_mode = False
num_topics = 10
stoplist = []
dataset = []
data = []
labelall = ["梦想","时光","感想","家乡","爱情"]
label = ["梦想","梦想","梦想","梦想","梦想","梦想","梦想","梦想","梦想","梦想","时光","时光","时光","时光","时光","时光","时光","时光","时光","时光","感想","感想","感想","感想","感想","感想","感想","感想","感想","感想","家乡","家乡","家乡","家乡","家乡","家乡","家乡","家乡","家乡","家乡","爱情","爱情","爱情","爱情","爱情","爱情","爱情","爱情","爱情","爱情"]
# print(len(label))
pattern = re.compile(r'[\u4e00-\u9fa5]+')

with open("data\\stopword.html", 'r', encoding='utf-8') as f:
    f = f.read()
    f = pattern.findall(f)
    stoplist = f[3:]
    print("finish building the stoplist")

with open("data\\rap.txt", 'r', encoding='utf-8') as f:
    f = f.read().replace(" ",'').split("\n")
    for lyrics in f:
        tmp1 = jieba.lcut(lyrics, cut_all=True)
        tmp2 = []
        for words in tmp1:
            if words not in stoplist and len(words) > 1:
                tmp2.append(words)  
        dataset.append(tmp2)
    print("finish building the dataset")

dictionary = corpora.Dictionary(dataset)
corpus = [dictionary.doc2bow(lyrics) for lyrics in dataset]
def train(corpus,dictionary,num_topics,label,labelall):
    lda = gensim.models.ldamodel.LdaModel(corpus=corpus,id2word=dictionary,num_topics=num_topics)
    print(lda.print_topics(num_topics=num_topics))
    lda.save("LDAmodel\\model")
    print("finish building the model")

    corpus_test = [dictionary.doc2bow(lyrics) for lyrics in dataset[:len(label)]]
    topics_test = lda.get_document_topics(corpus_test)

    for i in range(len(labelall)):
        tmp = []
        for j in range(num_topics):
            tmp.append(0)
        data.append(tmp)

    for i in range(len(label)):
        print("标签为:{}".format(label[i]))
        print("概率分布为:{}".format(topics_test[i]))
        tmp1 = labelall.index(label[i])
        for tuples in topics_test[i]:
            tmp2 = list(tuples)
            # print(tmp1)
            # print(tmp2)
            data[tmp1][tmp2[0]] += tmp2[1]

    #构造需要显示的值
    X=np.arange(0, len(labelall), step=1)#X轴的坐标
    Y=np.arange(0, num_topics, step=1)#Y轴的坐标
    Z=np.zeros(shape=(num_topics, len(labelall)))

    for i in range(num_topics):
        for j in range(len(labelall)):
            Z[i, j]=data[j][i]

    xx, yy=np.meshgrid(X, Y)#网格化坐标
    X, Y=xx.ravel(), yy.ravel()#矩阵扁平化
    bottom=np.zeros_like(X)#设置柱状图的底端位值
    Z=Z.ravel()#扁平化矩阵

    width=height=0.5#每一个柱子的长和宽

    #绘图设置
    fig=plt.figure()
    ax=fig.gca(projection='3d')#三维坐标轴
    ax.bar3d(X, Y, bottom, width, height, Z, shade=True)

    #坐标轴设置
    ax.set_xlabel('labalall')
    ax.set_ylabel('num_topics')
    ax.set_zlabel('value')
    plt.show()

def predict(corpus):
    labelnum = [[2,4,5,6],[0,8],[1,9,7],[3,4]]
    labelname = ['看法','爱情','家乡','时光']
    lda = gensim.models.ldamodel.LdaModel.load("LDAmodel\\model")
    topics = lda.get_document_topics(corpus)
    with open("data\\rap.txt", "r", encoding='utf-8') as f:
        f = f.read()
        f = f.split('\n')
        labeldata = []
        
        for i in range(len(topics)):
            maxnum = 0
            labeltopic = -1
            for tuple in topics[i]:
                tmp = list(tuple)
                if tmp[1] > maxnum:
                    maxnum = tmp[1]
                    labeltopic = tmp[0]
            if labeltopic != -1:
                for j in range(len(labelnum)):
                    if labeltopic in labelnum[j]:
                        f[i] = '一首写“' + labelname[j] + '”的歌：' + f[i]
                        break
        print(f[:10])
        f = '\n'.join(f)
        with open("data\\rapfinal.txt", "w", encoding='utf-8') as t:
            t.write(f)

if train_mode == True:
    train(corpus,dictionary,num_topics,label,labelall)

if train_mode == False:
    predict(corpus)
    





        





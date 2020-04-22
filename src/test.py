# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 13:34:19 2020

@author: Wayne
"""

import jieba
import jieba.analyse

text = '總統蔡英文論文風波延燒後，最新民調今日出爐！據親藍民調公布結果，蔡英文支持度45%，\
遙遙領先韓國瑜的33%，兩人差距擴大到12個百分點。顯示論文門風波，並未重創小英聲望。'
#
seg_list = jieba.cut(text, cut_all=False)
print(" / ".join(seg_list))

from snownlp import SnowNLP

s = SnowNLP(u'總統蔡英文論文風波延燒後，最新民調今日出爐！據親藍民調公布結果，蔡英文支持度45%，\
遙遙領先韓國瑜的33%，兩人差距擴大到12個百分點。顯示論文門風波，並未重創小英聲望。')
print(s.sentiments)

a1 = 235408
k1 = 179965
a2 = 394600
k2 = 186928
a3 = 387666
k3 = 221511
q = 491531

ans = (a1*k1)%q + (a2*k2)%q + (a3*k3)%q
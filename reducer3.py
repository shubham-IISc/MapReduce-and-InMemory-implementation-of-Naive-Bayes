#!/usr/bin/env python3

import sys
import math



sf=0.01
vsize=483243
prevword=None
word_label={}
index_label={}
word_prob={}



f = open("train_dict", 'r')
count_dict={}
lines = f.readlines();
for line in lines:
    line=line.strip()
    word,label,count = line.split('\t')
    if(word=="ANY"):
        count_dict[label]=int(count)
        
    else:
        break;


for line in sys.stdin:
    line=line.strip()
    word,label,count = line.split('\t')
    if(label[0]=='~'):
        label=label[1:]
    word=word.strip();
    if(label in count_dict.keys()):
        if(word!=prevword):
            word_label={}
            word_prob={}
            prevword=word
        word_label[label]=int(count);
    else:
        if(bool(word_label)):
            for l in count_dict.keys():
                if(word_label.get(l)==None):
                    if(word_prob.get(word+'^'+l)==None):
                        word_prob[word+'^'+l]=math.log(sf/(count_dict.get(l)+sf*vsize))
                    if(index_label.get(label+'^'+l)==None):
                        index_label[label+'^'+l]=int(count)*word_prob[word+'^'+l]
                    else:
                        index_label[label+'^'+l]=index_label[label+'^'+l]+int(count)*word_prob[word+'^'+l]
                else:
                    if(word_prob.get(word+'^'+l)==None):
                        word_prob[word+'^'+l]=math.log((word_label.get(l)+sf)/(count_dict.get(l)+sf*vsize))
                    if(index_label.get(label+'^'+l)==None):
                        index_label[label+'^'+l]= int(count)*word_prob[word+'^'+l]
                    else:
                        index_label[label+'^'+l]=index_label[label+'^'+l]+int(count)*word_prob[word+'^'+l]
                
for key,value in index_label.items():
    index,label=key.split('^')
    score=value
    print('%s\t%s\t%s' % (index,label,score))
                

#!/usr/bin/env python3

import sys
import math


# In[38]:
f = open("train_dict", 'r')
prior_dict={}
lines = f.readlines();
for line in lines:
    line=line.strip()
    word,label,count = line.split('\t')
    if(word=="PR_ANY"):
        prior_dict[label]=int(count)

    elif (word[0]>='a'):
        break;
total=sum(prior_dict.values())
for key,value in prior_dict.items():
    prior_dict[key]=value/total
final_dict={}

previndex=None
prevlabel=None
for line in sys.stdin:
    line=line.strip()
    index,label,score= line.split('\t')
    score=float(score)
    if(index!=previndex and label!=prevlabel):
        if(prevlabel!=None):
            totalscore=totalscore+math.log(prior_dict[prevlabel])
            if(totalscore>maxscore):
                final_dict[previndex]=prevlabel
        previndex=index
        prevlabel=label
        totalscore=score
        maxscore=-100000
    elif(index==previndex and label==prevlabel):
        totalscore=totalscore+score
    elif(index==previndex):
        totalscore=totalscore+math.log(prior_dict[prevlabel])
        if(totalscore>maxscore):
            maxscore=totalscore
            final_dict[index]=prevlabel
        prevlabel=label
        totalscore=score
for key,value in final_dict.items():
    print('%s\t%s' % (key,value))



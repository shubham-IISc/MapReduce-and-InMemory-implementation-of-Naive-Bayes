
# coding: utf-8

# In[40]:


import re
import string
import collections


# In[41]:



def cleanhtml(sentence): #function to clean the word of any html-tags
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', sentence)
    return cleantext
def cleanpunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    return  cleaned


# In[42]:


f=open('full_train.txt','r')


# In[43]:


d=f.readlines()
docs=[]
label=[]
for line in d:
    temp=line.split('\t')
    
    for l in temp[0].split(','):
        label.append(l.strip())
        docs.append(temp[1])
train_set=pd.DataFrame({})
train_set['docs']=docs
train_set['label']=label


# In[ ]:


str1=' '
final_string=[]
s=''
for sent in train_set['docs'].values:
    filtered_sentence=[]
    #print(sent);
    sent=cleanhtml(sent) # remove HTMl tags
    for w in sent.split():
        for cleaned_words in cleanpunc(w).split():
            if((cleaned_words.isalpha()) & (len(cleaned_words)>2)):    
                if(cleaned_words.lower()):
                    s=(cleaned_words.lower()).encode('utf8')
                    filtered_sentence.append(s)
                else:
                    continue
            else:
                continue 
    str1 = b" ".join(filtered_sentence) 
    
    final_string.append(str1)
train_set['CleanedDocs']=final_string 
train_set['CleanedDocs']=train_set['CleanedDocs'].str.decode("utf-8")


# In[ ]:


train_set.head()


# In[17]:


train_set['label']=pd.Categorical(train_set.label)
train_set['coded_label'] = train_set.label.cat.codes
decoded_label_list=train_set.label.cat.categories
total_labels=len(set(train_set.coded_label.values))
print(decoded_label_list)


# In[18]:


train_set.head(50)


# In[19]:


word_count_list=[]
for l in range(total_labels):
    word_count_list.append(collections.Counter([y for x in train_set[train_set['coded_label']==l].CleanedDocs.values.flatten() for y in x.split()]))


# In[20]:


[y for x in train_set[train_set['coded_label']==l].CleanedDocs.values.flatten() for y in x.split()]


# In[21]:


priorlist=[]
for l in range(total_labels):
    priorlist.append((train_set[train_set['coded_label']==l]).shape[0]/train_set.shape[0])


# In[22]:


print((train_set[train_set['coded_label']==11]).shape[0]/train_set.shape[0])


# In[23]:


print(priorlist)


# In[24]:


print(np.array(priorlist).sum())


# In[25]:


sum(word_count_list[1].values())


# In[26]:


total_word_list=[]
vocab_total=[]
for l in range(total_labels):
    total_word_list.append(sum(word_count_list[l].values()))
    vocab_total.extend((word_count_list[l].keys()))
vocab_total=set(vocab_total)
vocab_total_length=len(vocab_total)


# In[35]:


## word_count_list[{}] contain list of dictionaries of wordcounts corresponding to each class
## vocab_length_list[],vocab_total[],vocab_total_length
## predict for dev set 

f=open('full_devel.txt','r')
d=f.readlines()
docs=[]
label=[]
for line in d:
    temp=line.split('\t')
    label.append(temp[0].strip().split(','))
    docs.append(temp[1])

dev_set=pd.DataFrame({})
dev_set['label']=label
dev_set['docs']=docs











# In[36]:


str1=' '
final_string=[]
s=''
for sent in dev_set['docs'].values:
    filtered_sentence=[]
    #print(sent);
    sent=cleanhtml(sent) # remove HTMl tags
    for w in sent.split():
        for cleaned_words in cleanpunc(w).split():
            if((cleaned_words.isalpha()) & (len(cleaned_words)>2)):    
                if(cleaned_words.lower()):
                    s=(cleaned_words.lower()).encode('utf8')
                    filtered_sentence.append(s)
                else:
                    continue
            else:
                continue 
    str1 = b" ".join(filtered_sentence) 
    
    final_string.append(str1)
dev_set['CleanedDocs']=final_string 
dev_set['CleanedDocs']=dev_set['CleanedDocs'].str.decode("utf-8")


# In[37]:


vocab_counter=collections.Counter(vocab_total)


# In[38]:


smoothing=0.01


# In[39]:


#calculating log probabilities word-wise
from datetime import datetime
start=datetime.now()
def log_prob(x):
    ans=[];
    for l in range(total_labels):
        if(word_count_list[l][x]!=0):
            count=word_count_list[l][x]+smoothing
        elif(vocab_counter[x]!=0):
            count=smoothing
        else:
            count=0
            return np.zeros(total_labels)
        ans.append(np.log(count/(total_word_list[l]+(smoothing*vocab_total_length))))
    return np.array(ans)
#predicting class for dev set
pred=[]
for d in dev_set.CleanedDocs.values:
    total_prob=np.log(priorlist)
    wordlist=d.split()
    for w in wordlist:
        total_prob=total_prob+log_prob(w)
    pred.append(decoded_label_list[np.argmax(total_prob)])
dev_set['pred']=pred
#find accuracy
correct=0
for i in range(dev_set.shape[0]):
    if(dev_set['pred'][i] in dev_set['label'][i]):
        correct=correct+1
print(correct/dev_set.shape[0])


# In[442]:





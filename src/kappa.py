#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
annotation = pd.read_pickle("data\\Manual_Annotation\\annot_ID_dict.pkl")


# In[12]:


def makearray(a):
    res =[0]*60
    res = np.array(res).reshape(20,3)
    j=0
    for i in a.keys():
        if (a[i]["ahmad"]==1):
            res[j][0]+=1
        elif(a[i]["ahmad"]==0):  
            res[j][1]+=1
        elif(a[i]["ahmad"]==-1):  
            res[j][2]+=1            
        if (a[i]["severin"]==1):
            res[j][0]+=1
        elif(a[i]["severin"]==0):  
            res[j][1]+=1
        elif(a[i]["severin"]==-1):  
            res[j][2]+=1       
        if (a[i]["sina"]==1):
            res[j][0]+=1
        elif(a[i]["sina"]==0):  
            res[j][1]+=1
        elif(a[i]["sina"]==-1):  
            res[j][2]+=1   
        if (a[i]["ute"]==1):
            res[j][0]+=1
        elif(a[i]["ute"]==0):  
            res[j][1]+=1
        elif(a[i]["ute"]==-1):  
            res[j][2]+=1  
        j+=1
    return res    


# In[13]:


def fleiss_kappa(M):
    """Computes Fleiss' kappa for group of annotators.
    :param M: a matrix of shape (:attr:'N', :attr:'k') with 'N' = number of subjects and 'k' = the number of categories.
        'M[i, j]' represent the number of raters who assigned the 'i'th subject to the 'j'th category.
    :type: numpy matrix
    :rtype: float
    :return: Fleiss' kappa score
    """
    N, k = M.shape  # N is # of items, k is # of categories
    n_annotators = float(np.sum(M[0, :]))  # # of annotators
    tot_annotations = N * n_annotators  # the total # of annotations
    category_sum = np.sum(M, axis=0)  # the sum of each category over all items

    # chance agreement
    p = category_sum / tot_annotations  # the distribution of each category over all annotations
    PbarE = np.sum(p * p)  # average chance agreement over all categories

    # observed agreement
    P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))
    Pbar = np.sum(P) / N  # add all observed agreement chances per item and divide by amount of items

    return round((Pbar - PbarE) / (1 - PbarE), 4)


# In[14]:


print(fleiss_kappa(makearray(annotation)))


# In[ ]:





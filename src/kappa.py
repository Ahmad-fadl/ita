#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np


def makearray(a,n):
    team = ["ahmad", "severin", "sina", "ute"]
    res = [0] * n * 3
    res = np.array(res).reshape(n, 3)
    j = 0
    for i in a.keys():
        for member in team:
            if a[i][member] == 1:
                res[j][0] += 1
            elif a[i][member] == 0:
                res[j][1] += 1
            elif a[i][member] == -1:
                res[j][2] += 1
        j += 1
    return res


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


if __name__ == '__main__':
    # 1. kappa test with 20 tweets (baseline before group discussion)
    n=int(input('how many tweets do you want to calculate kappa for'))
    annotation = pd.read_pickle("data\\Manual_Annotation\\annot_ID_dict_3._kappa_test_50.pkl")
    print(fleiss_kappa(makearray(annotation,n)))
    #print(annotation)
    # 3. kappa test with 50 tweets
    # annotation = pd.read_pickle("data\\Manual_Annotation\\annot_ID_dict_3._kappa_test_50.pkl")
    # print(fleiss_kappa(makearray(annotation)))
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 10:33:15 2019

@author: Zixuan Huang
"""

import pandas as pd
import numpy as np

def onehot_converter(feature):
    #print(feature.shape)
    length = feature.shape[0]
    maximum = feature.max()
    minimum = feature.min()
    assert maximum <= 52
    assert minimum >= 0
    oh = np.zeros((length, 53)).astype(float)
    #print(oh.shape)
    oh[np.arange(length), feature] = 1
    return oh

def feat(df, bag=None, bag_length=500):
    idx1 = 1    # token, should be string
    idx2 = 3    # prefix, should be string
    idx3 = 4    # suffix, should be string
    label_idx = 5 # label
#    feat_list = []
#    feat_type = ['string', 'int', 'float', 'string', 'boolean']
#    for i in range(len(feat_type)):
#        df_np = df.as_matrix(columns=df.columns[i:i+1])
#        if feat_type[i] == 'string':
#            df_np = df.astype(str)
#        elif feat_type[i] == 'int':
#            df_np = df.astype(int)
#        elif feat_type[i] == 'float':
#            df_np = df.astype(int)
#        elif feat_type[i] == 'boolean':
#            df_np = df.astype(bool)
#        length = df_np.shape[0]
#        df_np = df_np.reshape(length)
#        feat_list.append(df_np)
    df_np = df.as_matrix(columns=df.columns[0:])
    #print(df_np.shape)
    length = df_np.shape[0]
    feat_size = df_np.shape[1]
    
    # Feat 1: Which letter to start with(0-26, containing other symbol as zeros)
    s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    tokens = df_np[:, idx1]
    first_letter = []
    for i in range(length):
        fl = tokens[i][0]
        fl_idx = s.find(fl) + 1
        first_letter.append(fl_idx)
    first_letter = np.array(first_letter)
    
    # Feat 2: Which letter to end up with(0-26, containing other symbol as zeros)
    last_letter = []
    for i in range(length):
        ll = tokens[i][-1]
        ll_idx = s.find(ll) + 1
        last_letter.append(ll_idx)
    last_letter = np.array(last_letter)
    
    # Feat 3: Length of token
    t_length = []
    for i in range(length):
        tmp = len(tokens[i])
        t_length.append(tmp)
    t_length = np.array(t_length)
    
    # Feat 4: Which letter in prefix to start with(0-26, containing other symbol as zeros)
    prefixes = df_np[:, idx2]
    first_letter_p = []
    for i in range(length):
        fl = prefixes[i][0]
        fl_idx = s.find(fl) + 1
        first_letter_p.append(fl_idx)
    first_letter_p = np.array(first_letter_p)
    
    # Feat 5: Which letter in prefix to end up with(0-26, containing other symbol as zeros)
    last_letter_p = []
    for i in range(length):
        ll = prefixes[i][0]
        ll_idx = s.find(ll) + 1
        last_letter_p.append(ll_idx)
    last_letter_p = np.array(last_letter_p)
    
    # Feat 6: Length of prefix
    p_length = []
    for i in range(length):
        tmp = len(prefixes[i])
        p_length.append(tmp)
    p_length = np.array(p_length)
    
    # Feat 7: Which letter in suffix to start with(0-26, containing other symbol as zeros)
    suffixes = df_np[:, idx3]
    first_letter_s = []
    for i in range(length):
        fl = suffixes[i][0]
        fl_idx = s.find(fl) + 1
        first_letter_s.append(fl_idx)
    first_letter_s = np.array(first_letter_s)
    
    # Feat 8: Which letter in suffix to end up with(0-26, containing other symbol as zeros)
    last_letter_s = []
    for i in range(length):
        ll = suffixes[i][0]
        ll_idx = s.find(ll) + 1
        last_letter_s.append(ll_idx)
    last_letter_s = np.array(last_letter_s)
    
    # Feat 9: Length of suffix
    s_length = []
    for i in range(length):
        tmp = len(suffixes[i])
        s_length.append(tmp)
    s_length = np.array(s_length)
    
    # Feat 10: Contain dash in token
    has_dash = []
    for i in range(length):
        tmp = tokens[i].find('-')
        if tmp == -1:
            has_dash.append(0.0)
        else:
            has_dash.append(1.0)
    has_dash = np.array(has_dash).astype(float)
    
    # Feat 11: Mr, etc in prefix
    mr_pref = []
    for i in range(length):
        if prefixes[i].lower() in ['executive', 'mr', 'dr', 'sir', 'minister', 'secretary', 'president', 'ms', 'mrs', 'who'] or suffixes[i].lower() in ['who']:
            mr_pref.append(1)
        else:
            mr_pref.append(0)
    mr_pref = np.array(mr_pref).astype(float)
    
    # Feat 12: said and other verb
    verb_pref = []
    for i in range(length):
        if prefixes[i].lower() in ['said', 'says', 'told', 'tell', 'tells'] or suffixes[i].lower() in ['said', 'says', 'has', 'had', 'told', 'tell']:
            verb_pref.append(1)
        else:
            verb_pref.append(0)
    verb_pref = np.array(verb_pref).astype(float)
    
    # Feat 13: Prefix contain '. or ! or ?'
    dot_pref = []
    for i in range(length):
        if prefixes[i][-1] in ['.', '!', '?', ':']:
            dot_pref.append(1)
        else:
            dot_pref.append(0)
    dot_pref = np.array(dot_pref).astype(float)
    #print(str(dot_pref.sum()/(float)(length))+'per cents have dot features!\n')
    
    # Feat 14: Two continuous uppercase
    upper_token = []
    for i in range(length):
        tmp = 0.0
        for j in range(len(tokens[i])-1):
            if tokens[i][j].isupper() and tokens[i][j+1].isupper():
                tmp = 1.0
        upper_token.append(tmp)
    upper_token = np.array(upper_token).astype(float)

    # Feat 15: belonging
    belong_pref = []
    for i in range(length):
        if suffixes[i].lower() == 's':
            belong_pref.append(1)
        else:
            belong_pref.append(0)
    belong_pref = np.array(belong_pref).astype(float)
    #print(belong_pref.sum())
    
    # Feat 16: Token Bag-of-Word
    if bag is None:
        bag = []
        count = []
        for i in range(length):
            if tokens[i] not in bag:
                bag.append(tokens[i])
                count.append(1)
            else:
                idx = bag.index(tokens[i])
                count[idx] += 1
            if prefixes[i] not in bag:
                bag.append(prefixes[i])
                count.append(1)
            else:
                idx = bag.index(prefixes[i])
                count[idx] += 1
            if suffixes[i] not in bag:
                bag.append(suffixes[i])
                count.append(1)
            else:
                idx = bag.index(suffixes[i])
                count[idx] += 1
        zipped = list(zip(bag, count))
        sorted_zipped = sorted(zipped, key=lambda x:x[1], reverse=True)
        bag, count = zip(*sorted_zipped)
        bag = list(bag)
        count = list(count)
        bag = bag[:bag_length]
        count = count[:bag_length]
        #print('Minumum count in the selected bag subset is %d' % count[-1])
    vec_len = len(bag)
    print('vec_len: '+str(vec_len))
    assert vec_len==bag_length
    #import pdb
    #pdb.set_trace()
    vec = np.zeros((length, vec_len))
    for i in range(length):
        if tokens[i] in bag:
            tmp = bag.index(tokens[i])
            vec[i, tmp] = 1    

    # Feat 17: Prefix Bag-of-Word
    vec_pref = np.zeros((length, vec_len))
    for i in range(length):
        if prefixes[i] in bag:
            tmp = bag.index(prefixes[i])
            vec_pref[i, tmp] = 1  

    # Feat 18: Suffix Bag-of-Word
    vec_suff = np.zeros((length, vec_len))
    for i in range(length):
        if suffixes[i] in bag:
            tmp = bag.index(suffixes[i])
            vec_suff[i, tmp] = 1   

    # One-hot processing
    first_letter = onehot_converter(first_letter)
    last_letter = onehot_converter(last_letter)
    t_length = t_length.astype(float).reshape(length, 1)
    first_letter_p = onehot_converter(first_letter_p)
    last_letter_p = onehot_converter(last_letter_p)
    p_length = p_length.astype(float).reshape(length, 1)
    first_letter_s = onehot_converter(first_letter_s)
    last_letter_s = onehot_converter(last_letter_s)
    s_length = s_length.astype(float).reshape(length, 1)
    has_dash = has_dash.reshape(length, 1)
    mr_pref = mr_pref.reshape(length, 1)
    verb_pref = verb_pref.reshape(length, 1)
    dot_pref = dot_pref.reshape(length, 1)
    upper_token = upper_token.reshape(length, 1)
    belong_pref = belong_pref.reshape(length, 1)

    feature = np.hstack((
        first_letter, 
        last_letter, 
        t_length, 
        first_letter_p, 
        last_letter_p, 
        p_length, 
        first_letter_s, 
        last_letter_s, 
        s_length, 
        has_dash, 
        mr_pref, 
        verb_pref, 
        dot_pref, 
        upper_token, 
        belong_pref,
        #vec,
        #vec_pref,
        #vec_suff
        ))    
    #feature = np.hstack((first_letter, last_letter, t_length, has_dash, mr_pref, verb_pref, dot_pref))
    
    # Generating labels
    labels = df_np[:, label_idx].astype(float)
    
    
    return feature, labels, bag
    


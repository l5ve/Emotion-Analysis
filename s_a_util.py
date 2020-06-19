#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os


# In[2]:



    
def start_analysis_v2(song_list,emotion_words,result):
    
    """
    Start emotion analysis, in this function sentiment_analysis_v2 which is the core fucntion of analysis is called.
    
    Args:
        song_list(list): partial list of songs. number of songs in list is entire songs(100)/ num of cores(4) = 25
        emotion_words(dic): dictionary of NRC-Emotion-lexicon
        result(Queue) : global queue which is shared by multiple processes
    """
    
    for i in song_list:
        print('Being processed by ',os.getpid())
        result.put(sentiment_analysis_v2(i,emotion_words))

def sentiment_analysis_v2(song,emotion_dic):
    
    """
    Sentiment(emotion) analysis for a song.
    
    Args: 
          song(dic): dicionary for all informations of a song
          emotion_dic : dictionary of NRC-Emotion-lexicon
    
    Returns:
         song['title'](string) : title of song
         emo_dic(dic): scores of 8-emotions, 2-setiments and dominant emotion
    """
    
    # to reduce time, use addition by array
    result=[0,0,0,0,0,0,0,0,0,0,0] 
    
    for key,val in song['lyric'].items():
        if key in emotion_dic:
            result = [x+y for x,y in zip(result,emotion_dic[key]*val)]

    print(result)
            
    emo_dic = {'Positive':result[0],
              'Negative':result[1],
              'Anger':result[2],
              'Anticipation':result[3],
              'Disgust':result[4],
              'Fear':result[5],
              'Joy':result[6],
              'Sadness':result[7],
              'Surprise':result[8],
              'Trust':result[9],
              'Love': result[10]}
    
    print(emo_dic)
            
    # set dominant emotion
    max =0;
    dominant=None
    for i in ['Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust','Love']:
        if emo_dic[i]>max:
            max = emo_dic[i]
            dominant=i       
            
    if dominant =='Joy'or dominant =='Trust':
        if emo_dic['Joy']>emo_dic['Trust'] and emo_dic['Trust']>= 0.5*emo_dic['Joy']:
            dominant = 'Love'
            emo_dic['Love']+=emo_dic['Trust']
        elif emo_dic['Joy']<emo_dic['Trust'] and emo_dic['Joy']>=0.9*emo_dic['Trust']:
            dominant = 'Love'
            emo_dic['Love']+=emo_dic['Joy']        
            
    emo_dic['dominant_emo']=dominant
    
    
    
    return song['title'],emo_dic


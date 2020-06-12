#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os


# In[2]:


def start_analysis(song,emotion_words,result):
    '''
    Do sentiment analysis and store that result at variable 'result' which is shared by processors
    
    Args: song(dictionary) : dicionary for all informations of a song
          emotion_words(dic) :  dictionary of NRC-Emotion-lexicon
          result(multiprocessing.queues.Queue) : store emotion analysis result in this variable which is shared by processors 
          
    '''
    print(type(result))
    print(os.getpid(),'에 의해 처리중')
    result.put(sentiment_analysis_v2(song,emotion_words))
    
    
def start_analysis_v2(song_list,emotion_words,result):
    
    for i in song_list:
        print(os.getpid(),'에 의해 처리중')
        result.put(sentiment_analysis_v2(i,emotion_words))
        
   


# In[ ]:


def sentiment_analysis_v1(song,emotion_words):
    
    """
   Sentiment(emotion) analysis for a song.
   
   Args: song(dictionary) : dicionary for all informations of a song
         emotion_words(pandas.core.frame.DataFrame): dataframe of NRC-Emotion-lexicon 
         
   
   
   """
    
    for key, val in song['lyric'].items():
        for i, row in emotion_words.iterrows():
            if key == row['Words']:
                for j in ['Positive','Negative','Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust']:
                    if row[j]==1:
                        song['sentiment'][j]+=val
                        print(j,':',song['sentiment'][j])
                        
    # set dominant emotion
    max =0;
    for i in ['Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust']:
        if song['sentiment'][i]>max:
            max = song['sentiment'][i]
            dominant_emotion=i
    song['dominant_emo']=dominant_emotion
    emo_dic = {'Positive':song['sentiment']['Positive'],'Negative':song['sentiment']['Negative'],'Anger':song['sentiment']['Anger'],                        'Anticipation':song['sentiment']['Anticipation'],'Disgust':song['sentiment']['Disgust'],'Fear':song['sentiment']['Fear'],'Joy':song['sentiment']['Joy'],'Sadness':song['sentiment']['Sadness'],'Surprise':song['sentiment']['Surprise'],'Trust':song['sentiment']['Trust'],'dominant_emo':song['dominant_emo']}
    
    return song['title'],emo_dic


# In[ ]:


def sentiment_analysis_v2(song,emotion_dic):
    
    """
    Sentiment(emotion) analysis for a song.
    
    Args: 
          song(dictionary): dicionary for all informations of a song
          emotion_dic : dictionary of NRC-Emotion-lexicon
    
    Returns:
         song['title'](string) : title of song
         emo_dic(dic): scores of 8-emotions, 2-setiments and dominant emotion
    """
    
    # to reduce time, use addition by array
    result=[0,0,0,0,0,0,0,0,0,0] 
    for key,val in song['lyric'].items():
        if key in emotion_dic:
            result+=emotion_dic[key]*val
            
    emo_dic = {'Positive':result[0],
              'Negative':result[1],
              'Anger':result[2],
              'Anticipation':result[3],
              'Disgust':result[4],
              'Fear':result[5],
              'Joy':result[6],
              'Sadness':result[7],
              'Surprise':result[8],
              'Trust':result[9]}
    print(emo_dic)
            
    # set dominant emotion
    max =0;
    dominant=None
    for i in ['Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust']:
        if emo_dic[i]>max:
            max = emo_dic[i]
            dominant=i       
    emo_dic['dominant_emo']=dominant
    
    return song['title'],emo_dic


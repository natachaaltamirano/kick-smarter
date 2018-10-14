
# coding: utf-8

# In[4]:


#get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import json
import time
#from time import strftime
#from datetime import datetime
import matplotlib
#from IPython.core.display import clear_output
from sklearn.externals import joblib

import re

import nltk
#this following two lines should be uncommneted in webapp
#nltk.download('punkt')
#nltk.download('stopwords')



from nltk import sent_tokenize
from nltk.tokenize import word_tokenize

#from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))


# In[8]:


def get_parser(html):

    ### returns the parser given a raw html

    x=BeautifulSoup(html.text,"html.parser")

    return x


# In[885]:

def category(parser):
    ff=parser.find("div", id="content-wrap").find("div").attrs["data-initial"]
    cate=json.loads(ff)["project"]["category"]["parentCategory"]["name"]
    cate=cate.lower()
    return cate



def num_of_videos(parser,box):

    ### returns the number of videos for the different boxes
    ### This also checks for youtube videos  -- that are linked different in Kickstarter [NOT IN MVP]

    if box=="about":


        try:
            # Normal video
            a=len(parser.find('div',class_='full-description js-full-description responsive' + '-media formatted-lists'
            ).find_all('div', class_="video-player"))

            # YouTube Video
            #b=len(parser.find('div',class_='full-description js-full-description responsive' + '-media formatted-lists'
            #).find_all('div', class_="video-player"))

        except AttributeError:

            a=np.nan



        return a

    elif box=="risk":
        try:
            b= len(parser.find('div',class_='mb3 mb10-sm mb3 js-risks'
            ).find_all('div', class_="video-player"))
        except AttributeError:
            b=np.nan

        return b



# In[886]:


def num_of_pics(parser,box):

    ### returns the number of videos for the different boxes

    if box=="about":
        try:
            a= len(parser.find(
                'div',
                class_='full-description js-full-description responsive-media formatted-lists'
            ).find_all('img'))

        except AttributeError:

            a=np.nan

        return a


    elif box=="risk":
        try:

            b=len(parser.find('div',class_='mb3 mb10-sm mb3 js-risks'
                ).find_all('img'))


        except AttributeError:
            b=np.nan

        return b


# In[11]:


def is_pitch_video(parser):

    ### returns True is the pitching pic is a video and returns false otherwise

    obj=parser.find(
            'div',
            class_='mx-4 mx-12-md mx0-lg'
        ).find_all('div', class_="aspect-ratio aspect-ratio--16x9 w100p ksr-video-player bg-black")

    if len(obj)>=1:
        return True

    else:
        return False


# In[896]:


def num_of_perks(parser):

    ### returns the number of perks for a given campaing

    #This are the available perks

    try:
        perk=parser.find(
                    'div',
                    class_="NS_projects__rewards_list js-project-rewards"
                )

        perk_UF=perk.find_all("li",class_="hover-group pledge--inactive pledge-selectable-sidebar")


    # this is usefull for campaings that are already founded or unfounded
        if len(perk_UF) != 0:

            return len(perk_UF)
        # this is usefull for live campaings

        else:

            a=len(perk.find_all('li',class_="hover-group js-reward-available pledge--available pledge-selectable-sidebar"))

            # This are the perks that are gone -- For the MVP I will put them together but they might be

            b=len(perk.find_all('li',class_="hover-group pledge--all-gone pledge-selectable-sidebar"))

            return a+b

    except AttributeError:

        return np.nan


# In[13]:


def price_in_perks(parser):

    ### Returns an array of the amount asked for each perk in order of appearence

    # For available perks
    per=parser.find(
            'div',
            class_="NS_projects__rewards_list js-project-rewards"
        ).find_all('li',class_="hover-group js-reward-available pledge--available pledge-selectable-sidebar")

    l=[]
    for i in range(len(per)):

        r=per[i].find_all("span",class_="money")[0].text

        r=r.replace(",","")
        r=r.replace(".","")

        l.append([int(''.join(i)) for is_digit, i in groupby(r, str.isdigit) if is_digit][0])

    l=np.array(l)

    # For unavilable perks

    per1=parser.find(
            'div',
            class_="NS_projects__rewards_list js-project-rewards"
        ).find_all('li',class_="hover-group pledge--all-gone pledge-selectable-sidebar")

    if len(per1)==1:
        return l
    else:
        l1=[]
        for i in range(len(per)):

            r=per1[i].find_all("span",class_="money")[0].text

            r=r.replace(",","")
            r=r.replace(".","")

            l1.append([int(''.join(i)) for is_digit, i in groupby(r, str.isdigit) if is_digit][0])

        l1=np.array(l1)

        return np.concatenate((l,l1))


# In[874]:


def get_text(parser,box):

    ### Gets the text for a given box in the campaing.
    ### this will only clean basic html feature, remove bold, italic, etc
    ### it will keep the raw text

    if box=="about":

        try:
            text=parser.find(
                'div',
                class_='full-description js-full-description responsive-media formatted-lists'
            ).get_text(' ')

            text=" ".join(text.split()).strip()

        except AttributeError:

            text='NA'

        return text

    elif box=="risk":

        try:
            text=parser.find(
                'div',
                class_='mb3 mb10-sm mb3 js-risks'
            ).get_text(' ')

            text=" ".join(text.split()).strip()

        except AttributeError:

            text='NA'

        return text.strip("Risks and challenges").strip("Learn about accountability on Kickstarter")

    elif box=="perks":

        try:
            perk=parser.find(
                    'div',
                    class_="NS_projects__rewards_list js-project-rewards"
                )

            perk_UF=perk.find_all("li",class_="hover-group pledge--inactive pledge-selectable-sidebar")


        except AttributeError:

            tp="NA"
            return tp


        # this is usefull for campaings that are already founded or unfounded
        if len(perk_UF) != 0:

            try:

                tp=''

                for i in range(len(perk_UF)):
                    neetp=perk_UF[i].find_all(
                        "div",class_='pledge__reward-description pledge__reward-description--expanded')[0].get_text(' ')
                    tp=tp + neetp

                tp=" ".join(tp.split()).strip()

            except AttributeError:

                tp='NA'

                return tp

        else:

            try:
                a=perk.find_all('li',
                                class_="hover-group js-reward-available pledge--available pledge-selectable-sidebar")

                # This are the perks that are gone -- For the MVP I will put them together but they might be

                b=perk.find_all('li',class_="hover-group pledge--all-gone pledge-selectable-sidebar")

            except AttributeError:

                tp="NA"

                return tp

            try:

                tp=''
                for i in range(len(a)):
                    neetp=a[i].find_all(
                        "div",class_='pledge__reward-description pledge__reward-description--expanded')[0].get_text(' ')
                    tp=tp + neetp

                for i in range(len(b)):
                    neetp=b[i].find_all(
                        "div",class_='pledge__reward-description pledge__reward-description--expanded')[0].get_text(' ')
                    tp=tp + neetp

                tp=" ".join(tp.split()).strip()

            except AttributeError:

                tp='NA'
                return tp


        return tp





# In[118]:


def num_of_sentences(text):
    if text=="NA":
        return np.nan
    else:

        sentences = sent_tokenize(text)

        return len(sentences)


# In[468]:


def num_of_words(text):

    if text=="NA":

        return np.nan

    else:

        tokens = word_tokenize(text)

        #this removes all characters that are not words
        words = [word.lower() for word in tokens if word.isalpha()]

        return len(words)


# In[121]:


def num_of_links(parser,box):

    if box == 'about':
        try:
            return len(parser.find(
                'div',
                class_='full-description js-full-description responsive-media formatted-lists'
            ).find_all('a'))
        except AttributeError:

            return np.nan


    elif box == 'risk':
        try:
            return len(parser.find(
                'div',
                class_='mb3 mb10-sm mb3 js-risks'
            ).find_all('a'))-1
        except AttributeError:

            return np.nan


# In[729]:


def freq_of_bold(parser,box):

    '''returns #bold_words/#total_words for boxes "about" and " risks" '''

    if box=="about":

        text= get_text(parser,box)

        if text == "NA":

            return np.nan

        else:

            bold =parser.find(
                'div',
                class_='full-description js-full-description responsive-media formatted-lists'
            ).find_all("b")

            strong=parser.find(
                'div',
                class_='full-description js-full-description responsive-media formatted-lists'
            ).find_all("strong")

            words=" ".join([sentence.get_text() for sentence in bold]).strip()

            words_S=" ".join([sentence.get_text() for sentence in strong]).strip()

            words= words_S + " " + words
            #words = word_tokenize(words)
            words = word_tokenize(words)

            words=[word.lower() for word in words if word.isalpha()]

            if num_of_words(text)==0:
                frequency=0
            else:
                frequency=len(words)/num_of_words(text)



            return frequency*100


    elif box == "risk":

        text= get_text(parser,box)

        if text == "NA":

            return np.nan

        else:

            bold=parser.find(
                'div',
                class_='mb3 mb10-sm mb3 js-risks'
            ).find_all("b")

            words=" ".join([sentence.get_text() for sentence in bold]).strip()

            words = word_tokenize(words)

            words=[word.lower() for word in words if word.isalpha()]

            if num_of_words(text)==0:
                frequency=0
            else:
                frequency=len(words)/num_of_words(text)

            return frequency*100





# In[728]:


def freq_of_italic(parser,box):

    '''returns #bold_words/#total_words for boxes "about" and " risks" '''

    if box=="about":

        text= get_text(parser,box)

        if text == "NA":

            return np.nan

        else:

            bold =parser.find(
                'div',
                class_='full-description js-full-description responsive-media formatted-lists'
            ).find_all("i")

            words=" ".join([sentence.get_text() for sentence in bold]).strip()

            words = word_tokenize(words)

            words=[word.lower() for word in words if word.isalpha()]

            if num_of_words(text)==0:
                frequency=0
            else:
                frequency=len(words)/num_of_words(text)


            return frequency*100


    elif box == "risk":

        text= get_text(parser,box)

        if text == "NA":

            return np.nan

        else:

            bold=parser.find(
                'div',
                class_='mb3 mb10-sm mb3 js-risks'
            ).find_all("i")

            words=" ".join([sentence.get_text() for sentence in bold]).strip()

            words = word_tokenize(words)

            words=[word.lower() for word in words if word.isalpha()]

            if num_of_words(text)==0:
                frequency=0
            else:
                frequency=len(words)/num_of_words(text)

            return frequency*100


# In[617]:


def num_of_exclamation(parser,box):

    text= get_text(parser,box)

    if text == "NA":

        exclamation_num=np.nan

    else:

        words = word_tokenize(text)

        exclamation_num=words.count("!")

    return exclamation_num


# In[782]:


# From https://blog.hubspot.com/sales/sensory-words-to-spice-up-your-sales-pitch

Pitch_words="see picture appear outlook focus observe notice watch overview sound hear mention inquire tune listen vocal remark say report feel grasp firm pressure grip flow warm emotional active assume you value and or imagine remember results easy benefit improved solution proven thank because welcome free new first premium help save now safe better bargain instant powerful best risk sale tips"

Pitch_words=Pitch_words.split()

def freq_of_stopwords(parser,box):

    ### retruns #stop_words/#words for a given campaing in a given section

    text=get_text(parser,box)


    if text == "NA":

        freq=np.nan

    elif num_of_words(text)==0:

        freq=0.



    elif num_of_words(text)!=0:



        tokens = word_tokenize(text)

        #this removes all characters that are not words
        words = [word.lower() for word in tokens if word.isalpha()]

        freq=(len([w for w in words if w in stopWords])/len(words))*100


    return freq


# In[785]:


def freq_of_pitchwords(parser,box):

    ### retruns #stop_words/#words for a given campaing in a given section

    text= get_text(parser,box)

    if text == "NA":

        freq=np.nan

    elif num_of_words(text)==0:

        freq=0.

    else:

        tokens = word_tokenize(text)

        #this removes all characters that are not words
        words = [word.lower() for word in tokens if word.isalpha()]

        freq=(len([w for w in words if w in Pitch_words])/len(words))*100

    return freq


# In[ ]:


def get_goal(par):

    ## returns the value of the goal for a ginve campaing

    mon=par.find_all("span",class_="ksr-green-700")[0].text

    return int(''.join(c for c in mon if c.isdigit()))


# # Computing the features

# In[ ]:
catego=joblib.load("category_map.pkl")

def get_features(url):

    ### Returns the given features for a given url of the campaing


    new_features=["goal","code","num_videos","num_pics","num_perks","num_links",
              "num_of_sent_about","num_of_sent_risk","num_of_sent_perks",
             "num_of_words_about","num_of_words_risk",
             "freq_bold_A","freq_bold_R",
             "freq_italic_A","freq_italic_R",
             "num_of_exclamation_A","num_of_exclamation_R","num_of_exclamation_P",
             "bool_R",
             "freq_pitch_A","freq_pitch_R","freq_pitch_P","words_x_perk"]

    df_features=pd.DataFrame(columns=new_features)


    HTML= requests.get(url)


    par=get_parser(HTML)

    goal = get_goal(par)



    text_about=get_text(par,"about")
    text_risk=get_text(par,"risk")
    text_perks=get_text(par,"perks")

    category_par=category(par)


    code=catego[category_par]

    bR=1

    if text_risk=="NA":
        bR=0



    features=(goal,code,num_of_videos(par,"about"),num_of_pics(par,"about"),num_of_perks(par),num_of_links(par,"about"),
              num_of_sentences(text_about), num_of_sentences(text_risk),num_of_sentences(text_perks),
              num_of_words(text_about),num_of_words(text_risk),
              freq_of_bold(par,"about"),freq_of_bold(par,"risk"),
              freq_of_italic(par,"about"),freq_of_italic(par,"risk"),
              num_of_exclamation(par,"about"),num_of_exclamation(par,"risk"),num_of_exclamation(par,"perks"),
              bR,
              freq_of_pitchwords(par,"about"),freq_of_pitchwords(par,"risk"),freq_of_pitchwords(par,"perks"),
              num_of_words(text_perks)/num_of_perks(par))

    df_features.loc[0]=features

    return df_features

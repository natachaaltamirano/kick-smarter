from flask import render_template
from flask_trustkeeper import app
import pandas as pd
from flask import request
from random import randint


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.externals import joblib
import sys
#sys.path.insert(0, '/Users/natacha/Documents/Insight/flask_empty')
sys.path.insert(0, '../')
import random


import feature_extraction as fe
import plots as pl

RF_clf=joblib.load("trained_clf.pkl")
#catego=joblib.load("category_map.pkl")

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

from sklearn.metrics import confusion_matrix
import itertools

def predictions(url):
    ff=fe.get_features(url)
    prob=RF_clf.predict_proba(ff)[0][1]*100

    return prob,ff

@app.route('/')
@app.route('/index')
def index():
   return render_template("index.html",
      title = 'Home', user = { 'nickname': 'Jahir' },
      )

@app.route('/input')
def tag_input():
   return render_template("input.html")

@app.route('/resume')
def tag_resume():
   return render_template("resume.html")

@app.route('/output')
def tag_output():
 #pull 'tag' from input field and store it

   tag_input = request.args.get('tag_input')


   try:

      nam=random.randint(1,101)
      name_file=str(nam)+".png"
      tag_output = tag_input
      P,ff=predictions(str(tag_input))
      pred="{:.0f}%".format(P)


      pl.plot_recomendation(ff["num_perks"],ff["num_of_words_about"],ff["freq_bold_A"],
                      ff["words_x_perk"],ff["num_pics"],ff["num_links"])

      plt.savefig("flask_trustkeeper/static/"+name_file,bbox_inches='tight')

      fl=True
      #if ff["goal"]<10000:
      if fl==True:
          return render_template("outputKS.html",perc = pred, kurl = tag_output,variable_name=name_file)

      else:
          return render_template("outputKS_biggoal.html",perc = pred, kurl = tag_output,variable_name=name_file)

   except:
      tag_output = tag_input
      return render_template("output_error.html",kurl = tag_output)

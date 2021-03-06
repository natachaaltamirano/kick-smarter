# Kick-Smarter
## About
A machine learning tool that predicts the success of Kickstarter campaigns and suggests features to be improved. 

## Where to find it?
You can find Kick-Smarter [here](http://www.kick-smarter.net) and put your campaign's url and hit Try me!. 
You will be redirected to a page that shows the chances you have to succeed and compares your campaign with the most and less funded campaigns in Kickstarter. 

## The Kick-Smarter engine 

The predictions are based on a random forest classifiers that studies 22 meta and constructed features of your campaign. This model has been validated using 5-fold cross-validation and a validation set of Kickstarter campaigns of the past 5 years.

The recommendations are based on 4 classifiers algorithm's feature importance (precision weighted) to minimize false positives.

**Note:** Kick-smarter engine is based on US campaigns that have goals less than $10,000.


## Resources
- Jupyter notebooks to illustrate the pipeline of construction for the  Kick-Smarter engine
   1. [Getting meta data](https://github.com/natachaaltamirano/kick-smarter/blob/master/A_Metafeatures_using_avilable_data.ipynb)
   2. [Cleaning of meta data](https://github.com/natachaaltamirano/kick-smarter/blob/master/B_Further_cleaning.ipynb)
   3. [Scrape HTML of meta campaign](https://github.com/natachaaltamirano/kick-smarter/blob/master/C_Use_meta_data_to_scrape_web.ipynb)
   4. [Module for feature engineering](https://github.com/natachaaltamirano/kick-smarter/blob/master/D2_Saving_functions_as_pyfile_feature_extraction.ipynb)
   5. [Feature extraction of raw HTML](https://github.com/natachaaltamirano/kick-smarter/blob/master/D_Feature_engeneering_from_raw_HTML.ipynb)
   6. [Analysis of the data](https://github.com/natachaaltamirano/kick-smarter/blob/master/E_Feature_analysis.ipynb)
   7. [Model training and predictions](https://github.com/natachaaltamirano/kick-smarter/blob/master/F_Models.ipynb)
- A [Web app](https://github.com/natachaaltamirano/kick-smarter/tree/master/Flask_web_app) folder  that contains the Flask app for [kick-smarter.net](http://www.kick-smarter.net) deployed in AWS using Bootstrap.
- Two Python modules used by the [Web app](https://github.com/natachaaltamirano/kick-smarter/tree/master/Flask_web_app):
   1. `feature_extraction.py` contains all functions used for extraction of features
   2. `plots.py` contains code that generates the plot for feature suggestions. 

- The trained Random Forest classifier used in the [Web App](https://github.com/natachaaltamirano/kick-smarter/tree/master/Flask_web_app).


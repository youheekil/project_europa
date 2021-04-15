Final Project
==============================
This is a final project for MDA course in KU LEUVEN (2021)
### What do we expect from each Team ?
In a nutshell, we want you to think as a data-scientist throughout the whole production pipeline: retrieving & pre-processing data, exception handling, building a model, hyperparameter optimization, etc...
We expect that you bring the topics explained during the course into practice. Your team should be able to bring value to the data. You can use techniques that were not covered during the course and can bring other python packages into the project. 
Make sure you start from the same python environment, used in the course. Of course you can update packages, install new ones,...
Make sure that you understand the underlying mathematics in the approach that you use (supervised, unsupervised, nlp, AI,..). A data-scientist is much more than an expert in Sklearn, NLTK, Pytorch,etc...

# ECB Bond Purchases 

## Introduction 
The European Central Bank has been buying corporate bonds since 2015. This signifies an important cash injection in the European Economy. The ECB started buying assets from commercial banks as part of its non-standard monetary policy measures. These asset purchases, also known as quantitative easing or QE, support economic growth across the euro area and helps Europe to return to inflation levels below, but close to, 2%.

## Proposed Research Question
Has the European Central bank been supporting the green economy when purchasing corporate bonds ?

## Initial Dataset(s)
Data1: <https://www.ecb.europa.eu/mopo/implement/app/html/index.en.html#cspp> 

Data2: <https://sdw.ecb.europa.eu>

To find information of a sector / industry a company is belonging to, you might for example want to consult the Refinitiv database (API-available) <https://permid.org/>

### Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

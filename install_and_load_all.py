def install_and_load_all():
    import re, sys, imp
    # Loads all libraries. If a library is missing warns user

    try:
        import pandas as pd
        import matplotlib as mpl
        import numpy as np
        import seaborn as sb
        import hail as hl
        import scipy as sp
        import statsmodels as sm
        import bokeh as bk
        import sklearn as skl
        import nltk
        import keras

    except ModuleNotFoundError as me:
        misssing_module = re.search('''(?<=')\s*[^']+?\s*(?=')''', str(me))
        print(str(me)+". Please install"+" "+str(misssing_module.group().strip()) + '.')
        print("To install, use '!pip3 install --upgrade"+" "+ str(misssing_module.group().strip()) + "' and run code again.")
        print("If error persists, ensure module's name is correct.")
    

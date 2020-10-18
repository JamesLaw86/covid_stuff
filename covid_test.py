# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 14:31:13 2020

@author: james
"""

import pandas as pd
import matplotlib.pyplot as plt
from uk_covid19 import Cov19API

def get_population(df):
    """
    Long winded way of getting the actual population of a region
    We find it based on the case data
    """ 
    population = None
    total_cases = cases = df['cumCasesByPublishDate'][0]  #Only latest value populated
    for i in range(len(df)):
        case_rate = df['cumCasesBySpecimenDateRate'][i]
        #total_cases = df['cumCasesByPublishDate'][i]
        if pd.isna(case_rate) or pd.isna(total_cases):
            continue
        if case_rate == 0 or total_cases == 0:
            continue
        deaths = df['cumDeathsByDeathDate'][i]
        if pd.isna(deaths):
            continue
        population = 100000 * cases / case_rate
        break
    return population

def add_deaths_per_100k(df):
    """
    Add a deaths per 100 thousand column
    """
    population = get_population(df)
    series = 100000 * df['cumDeathsByDeathDate'] / population
    df['cumDeathsBySpecimenDateRate'] = series
    
def get_region_data(region):
    filters_ = ['areaName=' + region]
    api = Cov19API(filters=filters_, structure=get_structure())
    df = api.get_dataframe()
    add_deaths_per_100k(df)
    return df

def get_structure():
    cases_and_deaths = { "date": "date",
                     "areaName": "areaName",
                     "areaCode": "areaCode",
                     "newCasesByPublishDate": "newCasesByPublishDate",
                     "cumCasesByPublishDate": "cumCasesByPublishDate",
                     "newDeathsByDeathDate": "newDeathsByDeathDate",
                     "cumDeathsByDeathDate": "cumDeathsByDeathDate",
                     "cumCasesBySpecimenDateRate" : "cumCasesBySpecimenDateRate" }
    return cases_and_deaths

df_horsham = get_region_data('Horsham')


fig = plt.Figure()
ax = fig.add_subplot(1,1,1)
ax.plot(df_horsham['cumDeathsBySpecimenDateRate'])




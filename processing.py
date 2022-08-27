import pandas as pd
from matplotlib import axis, pyplot as plt
import numpy as np
import utils 
import matplotlib.pyplot as plot
import plotly.graph_objects as go
from dash import dcc
from datetime import datetime


def get_dataframes(country):
    jobs_df = pd.read_csv('LinkedIn_DataScience_{0}.csv'.format(country))
    data_science_names_list = utils.get_list_from_file('resources/data_science_naming_list.txt')
    machine_learning_names_list = utils.get_list_from_file('resources/machine_learning_naming_list.txt')

    index_list = ['DATA SCIENCE', 'MACHINE LEARNING']

    skills_list = utils.get_list_from_file('resources/skills_list.txt')
    keywords_and_phrases_list = utils.get_list_from_file('resources/keywords_list.txt')
    
    # initialize dataframes
    skills_df = utils.generate_dataframe(index_list, skills_list, country)
    phrases_df = utils.generate_dataframe(index_list, keywords_and_phrases_list, country)

    list_of_lists = [skills_list, keywords_and_phrases_list]
    # lists can have different lengths but we want to zip them together later for convenience, so this adds 
    # zeros onto the end of shorter lists which we ignore later
    new_list_of_lists = utils.return_lists_as_length_of_longest(list_of_lists=list_of_lists)

    data_science_jobs_count = 0
    ml_science_jobs_count = 0

    for index, row in jobs_df.iterrows():
        title = str(row['Title']).upper()
        row_index = ''


        # the row index is set based on 'Data Science' in the title second so that if the title contains both 'Machine Learning' 
        # and 'Data Science' then the count will be added to 'Data Science'
        row_index = utils.get_row_index(row_index, machine_learning_names_list, title)
        row_index = utils.get_row_index(row_index, data_science_names_list, title)

        description = row['Description']
        description_capitalized = str(description).upper()
        if row_index != '':
            if row_index == 'DATA SCIENCE': data_science_jobs_count += 1
            if row_index == 'MACHINE LEARNING': ml_science_jobs_count += 1
            for skillname, keyphrase in zip(new_list_of_lists[0], new_list_of_lists[1]): 
                utils.populate_df_if_found(skillname, description_capitalized, skills_df, row_index)         
                utils.populate_df_if_found(keyphrase, description_capitalized, phrases_df, row_index)             

    total = len(jobs_df)

    skills_df = (skills_df[skills_list]/total * 100).join(skills_df['COUNTRY'])
    phrases_df = (phrases_df[keywords_and_phrases_list]/total * 100).join(phrases_df['COUNTRY'])

    total_jobs_scraped = len(jobs_df)


    return [skills_df, phrases_df, total_jobs_scraped, data_science_jobs_count, ml_science_jobs_count]


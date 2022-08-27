import numpy as np
import pandas as pd 
import re


def get_list_from_file(filename):
    content_list = []
    with open(filename, "r") as file:
        line = file.readline()
        while line:
            content_list.append(line.replace('\n',''))
            line = file.readline()
    return content_list

def return_lists_as_length_of_longest(list_of_lists):
    max = -1
    new_list_of_lists = []
    for list in list_of_lists:
        length = len(list)
        if max < length:
            max = length

    for list in list_of_lists:
        length_diff = max - len(list)
        new_list = list.copy()
        if length_diff > 0:
            new_list.extend(np.zeros(length_diff))
        new_list_of_lists.append(new_list)
    return new_list_of_lists
    

def generate_dataframe(index_list, list_for_columns, country): 
    init_values = np.zeros(shape=(len(index_list), len(list_for_columns)))
    df = pd.DataFrame(init_values, columns=list_for_columns, index=index_list)
    df.loc[:,'COUNTRY'] = country
    return df

def get_row_index(input_index, names_list, title):
    row_index = input_index
    words_re = re.compile("|".join(names_list))
    if words_re.search(title):
        row_index = names_list[0]
    return row_index

def standardise_df(df):
    total = len(df)
    return df/total * 100

def populate_df_if_found(what_to_find, where_to_find, df, row_index):
    if what_to_find != 0 and what_to_find in where_to_find:
        df.loc[row_index, [what_to_find]] = df.loc[row_index, [what_to_find]] + 1


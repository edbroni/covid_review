import numpy as np
import pandas as pd

def equalize_data(data1, data2, data3='none'):
    '''Make data1 and data2 with the same size, return data variables.
    Input: data1, data2 - pandas series
    Return: data1, data2 - list with same size.
    '''
    if type(data3) != type(data1):
        result=data1.merge(data2,left_index=True, right_index=True)
    else:
        result=data1.merge(data2,left_index=True, right_index=True)
        result=result.merge(data3,left_index=True, right_index=True)

    try:
        return result.iloc[:,0].values, result.iloc[:,1].values, result.iloc[:,2]
    except:
        return result.iloc[:,0].values, result.iloc[:,1].values

def extract_data(dataframe,column,group,operation):
    '''Function to extract a column from a pandas DataFrame and perform a group
    and an opertion like sum, count, max or min
    Inputs: dataframe - a pandas dataframe input
            column - a column of the dataframe - string
            group - a column to apply a groupby operation - string
            operation - a certain math to do with the data after groupby
    Output: result - a pandas series'''
    col_extract = [column, group]
    if operation == 'max':
        result = dataframe[col_extract].groupby(group).max().dropna()
    elif operation == 'sum':
        result = dataframe[col_extract].groupby(group).sum().dropna()
    elif operation == 'count':
        result = dataframe[col_extract].groupby(group).count().dropna()
    elif operation == 'min':
        result = dataframe[col_extract].groupby(group).min().dropna()
    elif operation == 'mean':
        result = dataframe[col_extract].groupby(group).mean().dropna()
    else:
        raise ValueError('{operation} is not recognized, use min,max,mean,count or sum'.format(operation=repr(operation)))
    return result

def read_data(file_location='../data/owid-covid-data.csv', sep=','):
    '''Read a CSV file
    Input - file-location - string
    Output - a pandas dataframe'''

    #List of world and continents
    location_sep = ['Asia', 'Africa', 'Europe', 'European Union', 'International', 'Oceania', 'South America', 'Central America', 'North America', 'America', 'World']
    data = pd.read_csv(file_location,sep=sep)
    #Removing location with continents names and world
    data = data[~data.location.isin(location_sep)]

    return data

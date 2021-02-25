import pandas as pd
import numpy as np
import plotly.graph_objs as go

def equalize_data(data1, data2, data3='none'):
    '''Make data1 and data2 with the same size, return data variables.
    Input: data1, data2, data3 - pandas series
    Return: data1, data2, data3 - list with same size.
    '''
    if type(data3) != type(data1):
        result=data1[data1>0.001].merge(data2[data2>0.001],left_index=True, 
                                        right_index=True)
    else:
        result=data1[data1>0.001].merge(data2[data2>0.1],left_index=True,
                                        right_index=True)
        result=result.merge(data3[data3>0.001],left_index=True, right_index=True)

    try:
        return result.iloc[:,0].values, result.iloc[:,1].values, \
               result.index.to_list(), result.iloc[:,2].values
    except:
        return result.iloc[:,0].values, result.iloc[:,1].values, \
               result.index.to_list()

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
        raise ValueError('{operation} is not recognized, use min,max,mean,\
count or sum'.format(operation=repr(operation)))
    return result

def read_data(file_location='data/owid-covid-data.csv', sep=','):
    '''Read a CSV file
    Input - file-location - string
    Output - a pandas dataframe'''

    #List of world and continents
    location_sep = ['Asia', 'Africa', 'Europe', 'European Union', 'International',
                   'Oceania', 'South America', 'Central America', 'North America',
                   'America', 'World']

    try: #It will try to download first
        data = pd.read_csv('https://covid.ourworldindata.org/data/owid-covid-data.csv',
                           sep=sep)
    except:
        data = pd.read_csv(file_location,sep=sep)

    #Removing location with continents names and world
    data = data[~data.location.isin(location_sep)]

    return data


def graph_scatter_go(x_data,y_data,hovertext,title_x,title_y,z_data=[],title_z=""):
    '''Graph the specified data and return a scatter plot
    Input: x,y and z_data - a pandas dataframe
           title - A title to the graph - string
    Output: a dictionary with graph and layout
    '''

    if len(z_data) == 0:
        graph = []    
        graph.append(
          go.Scatter(
          x = x_data,
          y = y_data,
          hoverinfo = 'text',
          hovertext = hovertext,
          mode = 'markers',
          marker={'symbol': 'circle-open-dot',
                  'color': 'orange'},
          )
        )

    else:
        graph = []    
        graph.append(
          go.Scatter(
          x = x_data,
          y = y_data,
          hoverinfo = 'text',
          hovertext = hovertext,
          mode = 'markers',
          marker={'symbol': 'circle-open-dot',
                  'color': z_data,
                  'colorscale': 'rainbow',
                  'colorbar':{'title': title_z}
                  },
          )
        )


    layout = dict(xaxis = dict(title = title_x),
                yaxis = dict(title = title_y),
                )


    return graph, layout


def return_figures():
    """Creates plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the plotly visualizations

    """

    #Reading data with default parameters
    data = read_data()

    #Extracting the columns to use
    gdp_country = extract_data(data,'gdp_per_capita','location','max')
    population_density_country = extract_data(data,'population_density',
                                             'location','max')
    deaths_per_million_country = extract_data(data,'total_deaths_per_million',
                                             'location','max')
    development_index_country = extract_data(data,'human_development_index',
                                            'location','max')
    cases_per_million_country =  extract_data(data,'total_cases_per_million',
                                             'location','max')
    tests_country =  extract_data(data,'total_tests','location','max')

    #Figures
    figures=[]

    #Analyses to plot

    #First graph is different we removed the World data
    data = pd.read_csv('data/owid-covid-data.csv',',')
    x=data[data.location=="World"].date
    y=data[data.location=="World"].new_cases_smoothed
    data,layout = graph_scatter_go(x,y,y,'Date','Cases')
    figures.append(dict(data=data, layout=layout))

    analyses = [
                [gdp_country,cases_per_million_country],
                [np.log(gdp_country),np.log(cases_per_million_country)],
                [development_index_country,cases_per_million_country],
                [development_index_country,np.log(cases_per_million_country)],
                [np.log(gdp_country),np.log(deaths_per_million_country)],
                [development_index_country,np.log(deaths_per_million_country)],
                [np.log(tests_country),np.log(cases_per_million_country),
                 development_index_country],
                [np.log(tests_country),np.log(deaths_per_million_country),
                 development_index_country],
                [np.log(population_density_country),
                 np.log(cases_per_million_country),
                 development_index_country]
               ]


    for attributes in analyses:
        label_x = str(attributes[0].columns[0])
        label_y = str(attributes[1].columns[0])
        if len(attributes) == 2:
            x_edt,y_edt,texto = equalize_data(attributes[0],attributes[1])
            data,layout = graph_scatter_go(x_edt,y_edt,texto,label_x,label_y)

        else:
            label_z = str(attributes[2].columns[0])
            x_edt,y_edt,texto,z_edt = equalize_data(attributes[0],
                                                    attributes[1],
                                                    attributes[2])
            data,layout= graph_scatter_go(x_edt,y_edt,texto,label_x,label_y, 
                                          z_edt, label_z)

        figures.append(dict(data=data, layout=layout))

    return figures

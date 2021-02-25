Link to Webapp https://covid-views.herokuapp.com/
# Covid Thoughts Blog Post Data Dashboard

## Introduction

This is a project in development for the Udacity Data Scientist Nanodegree.

This routines visualizes data from Our World in Data Covid database. This version don't uses a API but try to download the data and if is not possible load a copy.
It's no the best solution and I will review later with a better solution or an API.
We use plotly to visualize the data.

## Using Flask + Pandas + Plotly

We use the combination of Python + Pandas + Plotly + Flask to read data, visualize and display data.
The html page uses bootstrap to style and we use this [blog](https://getbootstrap.com/docs/5.0/examples/blog/) template.

## Prerequisites

To install the flask app, you need:

    python3
    python packages in the requirements.txt file

Install the packages with

 pip install -r requirements.txt

## Running

Open a terminal, and go into the directory with the flask app files. Run python covid_thoughts.py in the terminal. Or python3 covid_thoughts.py
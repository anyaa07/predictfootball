# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gLib3fw8WC8DwpLbKRmvn7sITQINCNcx
"""

import io
from io import StringIO
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import requests
import streamlit as st

# Replace the URL below with the raw URL of your CSV file on GitHub
url = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB20.csv"
url2 = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB21.csv"
url3 = "https://raw.githubusercontent.com/anyaa07/QBs/main/QB22.csv"

# Read the CSV file into a DataFrame
QB20 = pd.read_csv(url)
QB21 = pd.read_csv(url2)
QB22 = pd.read_csv(url3)




# create file uploader for QB21 file
#qb20_file = st.file_uploader("Upload QB20 CSV file", type="csv")

# create file uploader for QB20 file
#qb21_file = st.file_uploader("Upload QB21 CSV file", type="csv")

#qb22_file = st.file_uploader("Upload QB22 CSV file", type="csv")

# create a button to rename columns


# merge data
QB21_2 = QB21.rename(columns={'Pass': 'Pass Yds', 'TD2': 'TD', 'INT2': 'INT', 'Att2': 'Att', 'Comp2': 'Comp', 'Year2': 'Year'})
QB20_2 = QB20.rename(columns={'TDs': 'TD', 'INTs': 'INT', 'Year3': 'Year'})
merged = pd.concat([QB20_2, QB21_2], axis=0, ignore_index=True)
merged2 = pd.concat([QB21_2, QB22], axis=0, ignore_index=True)
data = pd.merge(QB20, QB21, on=['Player', 'Team'])
data1 = pd.merge(data, QB22, on=['Player', 'Team'])

#data2 = pd.merge(data, Records, on='Team')


# create linear regression model
model = LinearRegression()
# loop through each player
for player in data1['Player'].unique():

    # fit model to player data, merge 20 and 21 for x, 21 and 22 for y
    X = merged[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
    y = merged2[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
    model.fit(X, y)

# predict 2023-24 season stats 
predicted_stats = model.predict(QB22[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']])

    
# assign predicted statistics to the corresponding columns -- 
# mask --> selects only the rows of data that correspond to the current player that is being looped through
#enumerate --> gets the index of each of the selected rows where the players name matches the player variable, and assigns predicted stats only to the correct rows
pass_yd_pts = 0.04
pass_td_pts = 4
int_pts = -2
for index, player in enumerate(data1['Player'].unique()):
    mask = (data1['Player'] == player)
    data1.loc[mask, 'Pass Yds_2023_24'] = predicted_stats[index][0]
    data1.loc[mask, 'TD_2023_24'] = predicted_stats[index][1]
    data1.loc[mask, 'INT_2023_24'] = predicted_stats[index][2]
    data1.loc[mask, 'Comp_2023_24'] = predicted_stats[index][3]
    data1.loc[mask, 'Att_2023_24'] = predicted_stats[index][4]
    fantasy_points = data1['Pass Yds_2023_24']*pass_yd_pts + data1['TD_2023_24']*pass_td_pts + data1['INT_2023_24']*int_pts
    data1.loc[mask, 'Fantasy_Points'] = predicted_stats[index][4]
#QBR Calculation
cp = (data1['Comp_2023_24'] / data1['Att_2023_24'] - 0.3) * 0.05
ypa = (data1['Pass Yds_2023_24'] / data1['Att_2023_24'] - 3) * 0.25
tdp = (data1['TD_2023_24'] / data1['Att_2023_24']) * 0.2
intp = (data1['INT_2023_24'] / data1['Att_2023_24']) * 0.25

data1['QBR'] = ((data1['Comp_2023_24'] - 30) / 20 + ((data1['Pass Yds_2023_24'] / data1['Att_2023_24']) - 3) * 0.25 + (data1['TD_2023_24']) * 0.2 + 2.375 - (data1['INT_2023_24'] * 0.25)) * 100 / 6 / 3

selected_columns = data1[['Team', 'Player', 'Pass Yds_2023_24', 'TD_2023_24', 'INT_2023_24', 'Comp_2023_24', 'Att_2023_24', 'QBR', 'Fantasy_Points']]
player_search = st.text_input("Enter the name of the player you want to search for:")

# filter data for player search
if player_search:
    if st.button('Search'):
        filtered_data = selected_columns[selected_columns.index == player_search][['Team', 'Player', 'Pass Yds_2023_24', 'TD_2023_24', 'INT_2023_24', 'Comp_2023_24', 'Att_2023_24', 'QBR', 'Fantasy_Points']]
        st.write(filtered_data)



# print the modified data frame
#st.write(selected_columns)
    
        
        
#QB_20 = st.file_uploader("Choose a file")
#QB_21 = st.file_uploader("Choose a file")
#QB_22 = st.file_uploader("Choose a file")

#if uploaded_file is not None:
#file_contents = stringio.read()
#st.write(stringio)
    # Add your code to process the file here

# load data
#QB20 = pd.read_csv(io.BytesIO(uploaded[QB_20]))
#QB21 = pd.read_csv(io.BytesIO(uploaded[QB_21]))
#QB22 = pd.read_csv(io.BytesIO(uploaded[QB_22]))
#Records = pd.read_csv(io.BytesIO(uploaded['Records.csv']))


# merge data
#QB21_2 = QB21.rename(columns={'Pass': 'Pass Yds', 'TD2': 'TD', 'INT2': 'INT', 'Att2': 'Att', 'Comp2': 'Comp', 'Year2': 'Year'})
#QB20_2 = QB20.rename(columns={'TDs': 'TD', 'INTs': 'INT', 'Year3': 'Year'})
#merged = pd.concat([QB20_2, QB21_2], axis=0, ignore_index=True)
#merged2 = pd.concat([QB21_2, QB22], axis=0, ignore_index=True)
#data = pd.merge(QB20, QB21, on=['Player', 'Team'])
#data1 = pd.merge(data, QB22, on=['Player', 'Team'])

#data2 = pd.merge(data, Records, on='Team')


    
# assign predicted statistics to the corresponding columns -- 
# mask --> selects only the rows of data that correspond to the current player that is being looped through
#enumerate --> gets the index of each of the selected rows where the players name matches the player variable, and assigns predicted stats only to the correct rows

# print the modified data frame

#mean_absolute_error(y, predicted_stats)
#mean_squared_error(y, predicted_stats)

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

# Assign weights to each dataframe
weight_20 = .5 # Weight for QB20
weight_21 = 1.5 # Weight for QB21
weight_22 = 1.5# Weight for QB22

# Add weight columns to each dataframe
QB20['Weight'] = weight_20
QB21['Weight'] = weight_21
QB22['Weight'] = weight_22

# merge data
QB21_2 = QB21.rename(columns={'Pass': 'Pass Yds', 'TD2': 'TD', 'INT2': 'INT', 'Att2': 'Att', 'Comp2': 'Comp', 'Year2': 'Year'})
QB20_2 = QB20.rename(columns={'TDs': 'TD', 'INTs': 'INT', 'Year3': 'Year'})
merged = pd.concat([QB20_2, QB22], axis=0, ignore_index=True)
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
    sample_weights_X = QB20['Weight'].values  # Weight for QB20 data
    sample_weights_y = QB22['Weight'].values  # Weight for QB22 data
    sample_weights = np.concatenate((sample_weights_X, sample_weights_y))
    model.fit(X, y, sample_weight=sample_weights)

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
    fantasy_points = data1['Pass Yds_2023_24'] * pass_yd_pts + data1['TD_2023_24'] * pass_td_pts + data1['INT_2023_24'] * int_pts
    data1.loc[mask, 'Fantasy_Points'] = predicted_stats[index][4]
#QBR Calculation
cp = (data1['Comp_2023_24'] / data1['Att_2023_24'] - 0.3) * 0.05
ypa = (data1['Pass Yds_2023_24'] / data1['Att_2023_24'] - 3) * 0.25
tdp = (data1['TD_2023_24'] / data1['Att_2023_24']) * 0.2
intp = (data1['INT_2023_24'] / data1['Att_2023_24']) * 0.25

data1['Pass Yds_2023_24'] = data1['Pass Yds_2023_24'].astype(int)
data1['TD_2023_24'] = data1['TD_2023_24'].astype(int)
data1['INT_2023_24'] = data1['INT_2023_24'].astype(int)
data1['Comp_2023_24'] = data1['Comp_2023_24'].astype(int)
data1['Att_2023_24'] = data1['Att_2023_24'].astype(int)

data1['QBR'] = ((data1['Comp_2023_24'] - 30) / 20 + ((data1['Pass Yds_2023_24'] / data1['Att_2023_24']) - 3) * 0.25 + (data1['TD_2023_24']) * 0.2 + 2.375 - (data1['INT_2023_24'] * 0.25)) * 100 / 6 / 3
data1['QBR'] = data1['QBR'].round(1).astype(float)
data1['Fantasy_Points'] = data1['Fantasy_Points'].round(1).astype(float)


selected_columns = data1[['Team', 'Player', 'Pass Yds_2023_24', 'TD_2023_24', 'INT_2023_24', 'Comp_2023_24', 'Att_2023_24', 'QBR', 'Fantasy_Points']]
st.write("Hello and welcome! In this application, you can input the name of a quarterback to see what stats that quarterback is predicted to have for the 2023-2024 season! (Made by Anya Nagpal)")
player_search = st.text_input("Enter the name of the quarterback you want to search for (ensure that the name is capitalized and spelled correctly):")

# filter data for player search
if player_search:
    if st.button('Search'):
        filtered_data = selected_columns[selected_columns['Player'] == player_search][['Team', 'Player', 'Pass Yds_2023_24', 'TD_2023_24', 'INT_2023_24', 'Comp_2023_24', 'Att_2023_24', 'QBR', 'Fantasy_Points']]
        st.write(filtered_data)
#st.write("How does this work?: A linear regression model was trained on 3+ seasons worth of data for 75 different quarterbacks, and tested on one season worth of data. From there, projected stats for the next season (2023-2024) were predicted, and accuracy was tested on the one season used as the testing set.")

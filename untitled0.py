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

# create file uploader for QB21 file
qb20_file = st.file_uploader("Upload QB20 CSV file", type="csv")

# create file uploader for QB20 file
qb21_file = st.file_uploader("Upload QB21 CSV file", type="csv")

qb22_file = st.file_uploader("Upload QB22 CSV file", type="csv")

# create a button to rename columns
if qb20_file and qb21_file and qb22_file:
    if st.button("Execute Code"):
        # read QB21 and QB20 files into DataFrames
        QB20 = pd.read_csv(qb20_file)
        QB21 = pd.read_csv(qb21_file)
        QB22 = pd.read_csv(qb22_file)

        # rename columns in QB21 and QB20 DataFrames
        QB21_2 = QB21.rename(columns={'Pass': 'Pass Yds', 'TD2': 'TD', 'INT2': 'INT', 'Att2': 'Att', 'Comp2': 'Comp', 'Year2': 'Year'})
        QB20_2 = QB20.rename(columns={'TDs': 'TD', 'INTs': 'INT', 'Year3': 'Year'})
        merged = pd.concat([QB20_2, QB21_2], axis=0, ignore_index=True)
        merged2 = pd.concat([QB21_2, QB22], axis=0, ignore_index=True)
        data = pd.merge(QB20, QB21, on=['Player', 'Team'])
        data1 = pd.merge(data, QB22, on=['Player', 'Team'])

        # display the renamed DataFrames
        st.write("QB21 with renamed columns")
        st.write(QB21_2)
        st.write("QB20 with renamed columns")
        st.write(QB20_2)
        pd.set_option('display.max_rows', None)
        
        # create linear regression model + fit model + predict
        model = LinearRegression()
# loop through each player
        for player in data1['Player'].unique():
            X = merged[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
            y = merged2[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']]
            model.fit(X, y)

# predict 2023-24 season stats 
        predicted_stats = model.predict(QB22[['Pass Yds', 'TD', 'INT', 'Comp', 'Att']])
    
# fantasy and qbr
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
    #print
        print(data1)
    
        
        
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

# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:32:12 2026

@author: micha
Output is F but with modified logic for submission
"""

import pandas as pd

# Define the target website URL
url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
outputlines = []
a_line = ""

# Extract all tables found on the page
tables = pd.read_html(url, encoding="utf-8")
#tables = pd.read_html(url)

# Print how many tables were found
#print(f"Total tables found: {len(tables)}")

# Display the first table found
first_table = tables[0]

first_table = first_table.drop(0) #drop header line

first_table.columns = ['X','CHAR','Y'] #add new header

#print(first_table)

#sort it for ease of use
first_table_sorted = first_table.sort_values(by=['Y', 'X'], ascending=[False,True])

#print(first_table_sorted)

#see how long each line is to be
line_length_max = first_table_sorted['X'].max()

for prep_line in range(0,int(line_length_max)+1):
    a_line = a_line + " "

#see how many lines max so can prep the string
number_of_rows = first_table_sorted['Y'].max()

for prep_line_string in range(0, int(number_of_rows)+1):
    outputlines.append(a_line)
    
for x_loc in range(int(number_of_rows), -1, -1):
    a_line = outputlines[x_loc]
    
    for table_rownum in range(0, len(first_table_sorted)):
        if int(first_table_sorted.iloc[table_rownum,2]) == x_loc:
            index = int(first_table_sorted.iloc[table_rownum,0])
            new_char = first_table_sorted.iloc[table_rownum,1]
            
            a_line = a_line[:index] + new_char + a_line[index + 1 :]

        outputlines[x_loc] = a_line

#print final output
for x_loc in range(int(number_of_rows), -1, -1):
    print(outputlines[x_loc])

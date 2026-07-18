# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 15:32:12 2026

@author: micha

output is "F"
"""

import pandas as pd

# Define the target website URL
url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
first_line = ""
next_line = ""
last_line = ""

# Extract all tables found on the page
tables = pd.read_html(url, encoding="utf-8")
#tables = pd.read_html(url)

# Print how many tables were found
print(f"Total tables found: {len(tables)}")

# Display the first table found
first_table = tables[0]

first_table = first_table.drop(0)

first_table.columns = ['X','CHAR','Y']

#print(first_table)

#sort it for ease of use
first_table_sorted = first_table.sort_values(by=['Y', 'X'], ascending=[False,True])

print(first_table_sorted)

#print line 0
for prep_line in range(0,len(first_table)):
    
    first_line = first_line + " "
    next_line = next_line + " "
    last_line = last_line + " "
    
print("X" + first_line + "X")
index = 0
new_char = ""

for x_loc in range(0,len(first_table)):
    
    if int(first_table_sorted.iloc[x_loc,2]) == 2:
        index = int(first_table_sorted.iloc[x_loc,0])
        new_char = first_table_sorted.iloc[x_loc,1]
        first_line = first_line[:index] + new_char + first_line[index + 1 :]
    
    if int(first_table_sorted.iloc[x_loc,2]) == 1:
        index = int(first_table_sorted.iloc[x_loc,0])
        new_char = first_table_sorted.iloc[x_loc,1]
        next_line = next_line[:index] + new_char + next_line[index + 1 :]
        
    if int(first_table_sorted.iloc[x_loc,2]) == 0:
        index = int(first_table_sorted.iloc[x_loc,0])
        new_char = first_table_sorted.iloc[x_loc,1]
        last_line = last_line[:index] + new_char + last_line[index + 1 :]
    
print(first_line)
print(next_line)
print(last_line)

#>>> generate summary for comparing 2 different branches:
#>>>    * file missing
#>>>    * new file
#>>>    * file changes size
#>>>    * file changes modified date/time
#>>>    * file changes location
#>>> import os
#>>> os.chdir(r'C:\Users\017680\downloads')
#>>> exec(open('C:/users/017680/downloads/compare_folders.py').read())
#

import os
import sqlite3
from datetime import datetime
target_folder = 'C:/Users/017680/git clone/airflow_dev02_20250724_v2'
print_folder_name_once = True

connection = sqlite3.connect(':memory:')

# Create a cursor to execute commands
cursor = connection.cursor()

# Example: Create a table and insert data
cursor.execute('CREATE TABLE branch_a (folder_name TEXT, file_name TEXT, file_size INTEGER, file_creation DATETIME)')

# Fetch data
#cursor.execute('SELECT * FROM users')
#print(cursor.fetchone())  # Output: (1, 'Alice')

def drill_down_folder(path):
    """
    Recursively walks through a folder structure and prints all files.
    """
    # os.walk traverses top-down by default
    for root, dirs, files in os.walk(path):
        print_folder_name_once = True
        #print(f"Directory: {root}")
        for file in files:
            # print folder name once if any file in the folder is yaml or sql
            if file.find(".sql") > 0 or file.find(".yaml") > 0:
                if print_folder_name_once == True:
                    print(f"Directory: {root}")
                    print_folder_name_once = False
                file_path = os.path.join(root, file)
                file_info = os.stat(file_path)
                size_in_bytes = file_info.st_size
                timestamp = file_info.st_ctime
                #cursor.execute('INSERT INTO branch_a VALUES (',root,',',file,','size_in_bytes,',',datetime.fromtimestamp(timestamp))
                insert_statement = "INSERT INTO branch_a VALUES ('"+root.strip()+"','"+file.strip()+"',"+str(size_in_bytes)+",'"+str(datetime.fromtimestamp(timestamp))+"')"
                cursor.execute(insert_statement)

# Example usage:
# Replace 'your_folder_path' with the actual path
if os.path.exists(target_folder):
    drill_down_folder(target_folder)
    # Fetch data
    cursor.execute('SELECT * FROM branch_a')
    print(cursor.fetchone())  # Output: (1, 'Alice')
    # Close connection (deletes the database)
    connection.close()
else:
    print("Folder not found.")

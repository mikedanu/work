# Source - https://stackoverflow.com/a/71690680
# Posted by Tom Brereton
# Retrieved 2026-02-17, License - CC BY-SA 4.0
#######################
# executed using Python Shell
#
#>>> import os
#>>> os.chdir(r'C:\Users\017680\downloads')
#>>> exec(open('C:/users/017680/downloads/simple_csv_splitter.py').read())
#

# assume filename extension is csv >> update this filename
source_filename = 'Historical_Data_May25'
file_size_bytes = os.path.getsize('Historical_Data_May25.csv')
file = open('C:/Users/017680/Downloads/' + source_filename + '.csv', 'r')
header = file.readline()
csvfile = file.readlines()
filename = 1
# start with 100000 [then check for filesize every 10 lines afterwards] >> not done
batch_size = 600000
# filesize can't be more than max_file_size (in MB) for Snowflake's limitation >>> not done!
max_file_size_MB = 250

max_file_split = int(file_size_bytes/1000/1000/max_file_size_MB) + 1

print('File is to be split into ', max_file_split);

#only writes the header for the 1st part
open(source_filename + '_splitsection_1.csv', 'w+').writelines(header)
file.close()

for i in range(len(csvfile)):
    if i % batch_size == 0:
        if filename == 1:
            open(source_filename + '_splitsection_' + str(filename) + '.csv', 'a+').writelines(csvfile[i:i+batch_size])
        else:
            open(source_filename + '_splitsection_' + str(filename) + '.csv', 'w+').writelines(csvfile[i:i+batch_size])
        file.close()
        filename += 1

print('Split process completed. Total number of lines read = ', i+1);

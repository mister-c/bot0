import commands;
import re;

import os;

VOLA_ROOM_ID = os.environ.get('VOLA_ROOM_ID');

# Scrape the volafile page to see what urls there are to download
command = "phantomjs ./build/volafile-scrapper/scrapper.js %s | egrep -o " \
        "'https.{1,3}volafile.org/get/.{13,15}/.{1,100}\.[a-zA-Z]{1,5}'" % VOLA_ROOM_ID;

print(command);

file_list_str = commands.getstatusoutput(command)[1];

print(file_list_str);

if(file_list_str):
    file_list = file_list_str.split('\n');
else:
    file_list = ();


# Download all the files
for file in file_list:
    print('its a file: ' + file);

    # Check if we already downloaded the file
    # If we already downloaded then we can skip it
    command = 'grep ' + file + ' vola_list.txt';
    cmd_out = commands.getstatusoutput(command);
    
    if(len(cmd_out) > 1 and cmd_out[1] and len(cmd_out[1]) > 0):
        print("already in the list");
        continue;
    
    # Download the file
    command = 'wget -c --directory-prefix ./img_queue/ ' + file;
    cmd_out = commands.getstatusoutput(command);
    print(cmd_out);

    # Add the file to our list so we dont download again
    command = 'echo ' + file + ' >> vola_list.txt'
    cmd_out = commands.getstatusoutput(command);
    print(cmd_out);

    

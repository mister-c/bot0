import commands;

import re;

# This should only run on funny images
IMAGE_TAG = "funny";

highest_index = 0;
index_c = 0;

# Find highest index
file_list_str = commands.getstatusoutput('ls ./img/ | grep ' + IMAGE_TAG)[1];
file_list_str = re.sub('[^0-9\n]', '',  file_list_str);
file_index_list = file_list_str.split('\n');

if(highest_index < max(file_index_list)):
    highest_index = max(file_index_list);
    index_c = int(highest_index);
    
print(highest_index);

# Move the files
file_list_str = commands.getstatusoutput('ls ./img_queue/')[1];
if file_list_str:
    file_list = file_list_str.split('\n');
else:
    file_list = ();

for file in file_list:
    index_c += 1;
    file_ext = '.jpg';
    
    clean_fn = re.sub(' ', '\ ', file);
    matches = re.search('(\..{1,5})$', clean_fn);

    if(matches and len(matches.groups()) > 0):
        file_ext = matches.group(1);
        print('setting file_ext to: ' + file_ext);
    else:
        print('uhhh... no matches... guessing jpg?');
    
    print('mv ./img_queue/' + clean_fn + ' ./img/funny_' + str(index_c).zfill(4) + file_ext);
    
    print(commands.getstatusoutput('mv ./img_queue/' + clean_fn + ' ./img/funny_' + str(index_c).zfill(4) + file_ext));
    # print commands.getstatusoutput('mv ' + file + ' ./img/funny_' + index_c + file_ext);


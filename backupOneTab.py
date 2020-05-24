import os
import shutil
from datetime import datetime

chromedata_path = 'C:/Users/<Username>/AppData/Local/Google/Chrome/User Data/Default/Local Storage/leveldb' # this is your Chrome data path (make sure to replace <Username> with your user's username)
local_path = '/path/to/backups/folder/' # put your backups folder path here (make sure to include the last backslash /)
exclude_file = 'LOCK' 

# get current time
now = datetime.now() # current date and time
date_time = now.strftime('%m-%d-%Y_%H-%M-%S')
print('date and time:', date_time)

# define src directory
src = chromedata_path

# make dest_parent and dest directories
dest_parent = local_path + date_time
os.mkdir(dest_parent)
print(dest_parent + ' created')
dest = dest_parent + '/leveldb'
os.mkdir(dest)
print(dest + ' created')

# copy ldb and log files from chromedata directory to local directory
print('copying from ' + src + ' to ' + dest)
src_files = os.listdir(src)
for file_name in src_files:
  if(file_name == exclude_file):
    continue
  full_file_name = os.path.join(src, file_name)
  if os.path.isfile(full_file_name):
    shutil.copy(full_file_name, dest)
    print('copied ' + file_name)

print('backup complete\n')
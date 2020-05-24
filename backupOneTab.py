import sys
import os
import shutil
from datetime import datetime

chromedata_path = 'C:/Users/<Username>/AppData/Local/Google/Chrome/User Data/Default/Local Storage/leveldb' # this is your Chrome data path (make sure to replace <Username> with your user's username)
local_path = '/path/to/backups/folder/' # put your backups folder path here (make sure to include the last backslash /)
exclude_file = 'LOCK' 

def backup():
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

def restore(index): # index is the index of the backup with 0 being the latest and 1 being the second latest
  # define dest directory
  dest = chromedata_path

  # define src directory
  backups = next(os.walk(local_path))[1]
  backups.reverse()
  src = local_path + backups[index] + '/leveldb'

  # getting file numbers from src
  src_files = os.listdir(src)
  src_files_compare = [file_name for file_name in src_files]

  # remove files not in src from dest
  print('removing files not in ' + src + ' from ' + dest)
  dest_files = os.listdir(dest)
  for file_name in dest_files:
    if(file_name == exclude_file):
      continue
    full_file_name = os.path.join(dest, file_name)
    if os.path.isfile(full_file_name) and file_name not in src_files_compare:
      os.remove(full_file_name)
      print('deleted ' + file_name)

  # copy ldb and log files from local directory to chromedata directory
  print('copying from ' + src + ' to ' + dest)
  for file_name in src_files:
    full_file_name = os.path.join(src, file_name)
    if os.path.isfile(full_file_name):
      shutil.copy(full_file_name, dest)
      print('copied ' + file_name)
  
  print('restore complete\n')

def main():
  args = sys.argv[1:]

  print()
  if len(args) == 0: # no args are input
    fn = input('Backup or restore? ').lower()
    print()
    if fn == 'backup':
      backup()
    elif fn == 'restore':
      index = int(input('Enter the backup ID: '))
      restore(index)
    else:
      print('Error: Function not found')
    print(input('Press \'Enter\' to exit'))
  elif len(args) > 0 and args[0] == '--backup': # '--backup' arg is input
    backup()
  elif len(args) > 0 and args[0] == '--restore': # '--restore <int>' args are input
    index = int(args[1])
    restore(index)

if __name__ == '__main__':
  main()
# Backup OneTab

> CAUTION: Restoring doesn't really work right now due to recent OneTab changes, so please refer to [this issue](https://github.com/itsjoshthedeveloper/backupOneTab/issues/1). I am working on a fix.

This is a python script that will allow you to automatically\* back up and manually restore your OneTab extension Chrome data.

\*With Windows Task Scheduler

## The problem

I have used OneTab for years and have saved more than one thousand links. However, one day, I opened up OneTab and all my links were gone. I tried finding a better extension, but I couldn't find one as simple and efficient as OneTab. So, I decided to make a script to automatically back up and manually restore my data.

## This repository includes

- Python script named `backupOneTab.py`
- A `backups` folder that contains a backup example

## How to use

1. Clone this repository.
2. Open `backupOneTab.py` using a text editor or IDE.
   - In line 6, replace `<Username>` with your system user's username. For example, my path is `C:/Users/joshc/AppData/Local/Google/Chrome/User Data/Default/Local Storage/leveldb`.
   - If you want to save your backups to another folder other than the one in this repository, in line 7, replace `./backups/` with your backups folder path (make sure to include the last backslash `/`).
3. Then, you can run the script using `python backupOneTab.py`.
4. If you want to automate the back ups (and use Windows), open up the Task Scheduler (search using the Windows key). Follow the steps below or watch this [tutorial](https://www.youtube.com/watch?v=n2Cr_YRQk7o&feature=emb_title).
   - In the left pane, click `Task Scheduler Library`.
   - In the right pane, click `Create Task...`
   - Name your Task.
   - Go to the `Actions` tab and click `New...` at the bottom.
   - Under Settings, for `Program/script` input your `python.exe` path. For example, my path is `C:\Python38-32\python.exe`.
   - For `Add arguments` input `backupOneTab.py --backup`.
   - For `Start in` input the path of the directory where your `backupOneTab.py` script is in. For example, my path is `D:\_W\_Web\BackupOneTab`.
   - Hit `OK`, go to the `Triggers` tab, and click `New...` at the bottom.
   - For `Begin the task` select `At log on`.
   - Under Settings, select `Specific user` make sure that is your username.
   - Hit `OK` twice, and it should work.
5. I also used `pyinstaller` to make an executable of my script to make it easier to run. Follow this [tutorial](https://datatofish.com/executable-pyinstaller/) to do that.

## The process

I first tried to use Selenium to automate a script that could go to the import-export.html extension page and copy the textarea data of the exported links. However, I learned that Selenium doesn't have access to extension pages (which are different from regular web pages). I tried using the `webdriver.ChromeOptions().add_extension()` method, but this just gave me a `PermissionError: [Errno 13] Permission denied`.

So, I then tried something else. I knew from this [helpful Reddit thread](https://www.reddit.com/r/chrome/comments/76k23b/onetab_lost_all_tabs_recovery/) that the OneTab data was stored in the mysterious files in `C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb`. So, I decided to make a script to back up (make a copy of) the files in that folder.

I first implemented `distutils.dir_util.copy_tree()` but would consistently get more `PermissionError: [Errno 13] Permission denied` when copying the `LOCK` file. So, I ended up just using `shutil.copy()` to back up the files. After some testing, I discovered that the `.ldb` and `.log` files held the OneTab data. But, for some reason, when I only restored those files, Chrome would act like I had just installed all my extensions and would annoyingly open all the extension first install pages. So, eventually, I just backed up every file except for `LOCK` and that fixed the problem. I also used `datetime` to create folders named with the date and time the backup was made and implemented this all into a `backup()` method.

From there, I created a `restore(index)` method to restore a backup of your choosing (chosen with the index parameter) into the Chrome `leveldb` folder. However, I found that Chrome would sometimes use different numbered `.ldb` and `.log` files to store its data. This meant that my backups and the current `leveldb` folder might have differently numbered `.ldb` and `.log` files (for example: `000005.ldb` vs. `000097.ldb`). This could become a problem because just copying over a backup's files into the `leveldb` folder might result in some excess files that weren't in the backup remaining. So, I made sure to remove all files in the current `leveldb` folder that weren't in the backup before copying over the backup.

Then, I created a `main` function to handle all the system arguments one could input when running the script to control either a backup or restore function.

To run the script automatically on a consistent basis, I used **Windows Task Scheduler**. I created a new Task where I set a new Action to run the script and a new Trigger to trigger the Task whenever my user logged on. I tried to figure out how to implement a user logoff Trigger, and some sources claim that you can implement a script using the Registry Editor, but I didn't try it because it seemed sketchy.

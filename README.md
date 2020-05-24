# Backup OneTab

This is a python script that will automatically\* back up and allow you to manually restore your OneTab extension Chrome data.

\*With Windows Task Scheduler

**The process**

I first tried to use Selenium to automate a script that could go to the import-export.html extension page and copy the textarea data of the exported links. However, I learned that Selenium doesn't have access to extension pages (which are different from regular web pages). I tried using the `webdriver.ChromeOptions().add_extension()` method, but this just gave me a `PermissionError: [Errno 13] Permission denied`.

So, I then tried something else. I knew from [this helpful Reddit thread](https://www.reddit.com/r/chrome/comments/76k23b/onetab_lost_all_tabs_recovery/) that the OneTab data was stored in the mysterious files in `C:\Users\<Username>\AppData\Local\Google\Chrome\User Data\Default\Local Storage\leveldb`. So, I decided to make a script to backup (make a copy of) the files in that folder.

I first implemented `distutils.dir_util.copy_tree()` but would consistently get more `PermissionError: [Errno 13] Permission denied` when copying the `LOCK` file. So, I ended up just using `shutil.copy()` to backup the files. After some testing, I discovered that the `.ldb` and `.log` files held the OneTab data. But, for some reason, when I only restored those files, Chrome would act like I had just installed all my extensions and would annoyingly open all the extension first install pages. So, eventually, I just backed up every file except for `LOCK` and that fixed the problem. I also used `datetime` to create folders named with the date and time the backup was made and implemented this all into a `backup()` method.

From there, I created a `restore(index)` method to restore a backup of your choosing (chosen with the index parameter) into the Chrome `leveldb` folder. However, I found that Chrome would sometimes use different numbered `.ldb` and `.log` files to store its data. This meant that my backups and the current `leveldb` folder might have differently numbered `.ldb` and `.log` files (for example: `000005.ldb` vs. `000097.ldb`). This could become a problem because just copying over a backup's files into the `leveldb` folder might result in some excess files that weren't in the backup remaining. So, I made sure to remove all files in the current `leveldb` folder that weren't in the backup before copying over the backup.

Then, I created a `main` function to handle all the system arguments one could input when running the script to control either a backup or restore function.

To run the script automatically on a consistent basis, I used **Windows Task Scheduler**. I created a new Task where I set a new Action to run the script and a new Trigger to trigger the Task whenever my user logged on. I tried to figure out how to implement a user logoff Trigger, and some sources claim that you can implement a script using the Registry Editor, but I didn't try it because it seemed sketchy.

You are an AI assistant helping a configuration manager track automated system changes. 

In the directory `/home/user/archives/`, there are three backup archives: `backup_v1.tar.gz`, `backup_v2.tar.gz`, and `backup_v3.tar.gz`. Due to a storage failure, some of these archives are corrupted and cannot be read. Exactly one of them is fully intact.

The intact archive contains a file named `changelog.txt`. This file contains multi-line configuration change records in the following format:
```
BEGIN_CHANGE
Author: <username>
Date: <YYYY-MM-DD>
Modified:
  <file_path_1>
  <file_path_2>
END_CHANGE
```
There can be any number of file paths under the `Modified:` section until `END_CHANGE` is reached.

Your task is to:
1. Identify the single uncorrupted `.tar.gz` archive in `/home/user/archives/`.
2. Write a Python script at `/home/user/parse.py` that reads a changelog from `stdin` and extracts a uniquely deduplicated, alphabetically sorted list of all file paths modified by the author `deploy_bot`.
3. Extract the contents of `changelog.txt` from the valid archive directly to standard output (do NOT extract it to the disk) and pipe it into your Python script.
4. Redirect the final standard output of your Python script to the file `/home/user/bot_changes.txt`.

`/home/user/bot_changes.txt` must contain exactly the unique file paths modified by `deploy_bot`, one path per line, in alphabetical order.
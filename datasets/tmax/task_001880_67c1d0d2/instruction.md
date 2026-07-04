You are acting as a backup administrator managing an archive server. You need to perform an audit of the backup files, fix encoding issues in older backup notes, and generate a final status report. 

All files are located under `/home/user/backups`. 

Please perform the following operations using standard Linux command-line tools (bash, awk, grep, find, tar, iconv, file, etc.) or any scripting language of your choice, and generate a final report at `/home/user/backup_report.txt`.

**Step 1: Archive Integrity Verification**
Traverse the directory `/home/user/backups/archives` to find all `.tar.gz` files. Check each archive for integrity. Record the absolute paths of the corrupted archives.

**Step 2: Multi-line Log Record Parsing**
Read the backup log file at `/home/user/backups/logs/job_history.log`. This log contains multi-line records separated by `---`. Each record has a `Job ID:` line and a `Status:` line (among others). Find all Job IDs where the status is `FAILED`.

**Step 3: Domain-specific format parsing (ELF)**
The backup data directory `/home/user/backups/data` contains various files. Users accidentally backed up compiled Linux executables (ELF files). Traverse this directory recursively, identify all ELF files (regardless of their extension), and record their absolute paths.

**Step 4: Character Encoding Conversion**
The directory `/home/user/backups/notes` contains old backup notes as `.txt` files encoded in `ISO-8859-1`. Convert the contents of all `.txt` files in this directory to `UTF-8` and overwrite the original files. Record the total number of files converted.

**Final Output Format**
Create the file `/home/user/backup_report.txt` exactly in the following format:

```
[Corrupted Archives]
<absolute_path_to_corrupted_archive_1>
<absolute_path_to_corrupted_archive_2>
...

[Failed Jobs]
<Job_ID_1>
<Job_ID_2>
...

[ELF Files]
<absolute_path_to_elf_file_1>
<absolute_path_to_elf_file_2>
...

[Converted Notes]
Total converted: <number>
```
Sort the paths and Job IDs in each section in ascending alphabetical/numerical order.
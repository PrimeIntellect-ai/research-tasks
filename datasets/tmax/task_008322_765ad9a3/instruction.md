You are acting as a backup administrator for a Linux system. Your task is to perform an incremental backup of application configuration files and generate a backup report in a specific format.

We have a directory of configuration files located at `/home/user/app_configs`. 
A previous backup was taken at a specific UNIX timestamp, which is recorded in the file `/home/user/last_backup.json`.

Write and execute a Python script that performs the following steps:
1. Read the `last_backup_time` (a UNIX timestamp float or integer) from `/home/user/last_backup.json`.
2. Search recursively through `/home/user/app_configs` for all files ending with `.json`.
3. Check the metadata (modification time) of each `.json` file. If the file's modification time (`st_mtime`) is strictly greater than the `last_backup_time`, it should be included in the incremental backup.
4. Copy all qualifying new or modified `.json` files to the directory `/home/user/backup_archive` (you must create this directory if it does not exist). You can place them flat inside `/home/user/backup_archive` (assume there are no filename collisions).
5. Generate a YAML report at `/home/user/backup_report.yaml` containing the details of the files you just backed up. You may use `pip install pyyaml` if you wish to use the `yaml` module. 

The YAML file must follow this exact structure:
```yaml
backed_up_files:
  - filename: "example.json"
    size: 1024
  - filename: "another.json"
    size: 2048
```
The files in the YAML report should be sorted alphabetically by their filename. The `size` should be the size of the file in bytes.

Make sure to execute your script so that the `backup_archive` directory is populated and the `backup_report.yaml` file is created.
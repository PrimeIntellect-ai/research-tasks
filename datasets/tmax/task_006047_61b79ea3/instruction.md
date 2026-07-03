You are an AI assistant helping a bioinformatics researcher organize their raw sequencing datasets.

I have an archive of sequencing data located at `/home/user/data_archive.tar`. The files inside currently use temporary sample IDs. I also have a configuration file located at `/home/user/mapping.ini` that contains the mapping between these temporary sample IDs and the actual patient IDs.

Please perform the following steps:
1. Extract the contents of `/home/user/data_archive.tar` into the directory `/home/user/extracted/`. (Create the directory if it doesn't exist).
2. Write a Python script at `/home/user/rename.py` that interprets the `mapping.ini` configuration file. The `.ini` file has a section called `[Renames]` where each key is a temporary ID and the value is the patient ID.
3. Your Python script should rename all files in `/home/user/extracted/` by replacing the temporary ID prefix in the filename with the corresponding patient ID from the config file. (For example, if the config maps `sample1` to `patient_x`, a file named `sample1_read1.fq` should be renamed to `patient_x_read1.fq`).
4. For every file successfully renamed, the Python script must print a line exactly matching this format to standard output:
   `RENAMED: <old_filename> -> <new_filename>`
   (Note: Use only the base filename, not the full path, in the output).
5. Run your Python script and redirect its standard output to create a log file at `/home/user/rename_log.txt`.

Ensure all operations are completed and the log file is correctly populated.
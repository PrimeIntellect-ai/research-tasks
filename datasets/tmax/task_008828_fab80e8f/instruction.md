You are tasked with helping a developer organize and catalog project files for an upcoming backup. There is a directory structure at `/home/user/projects` containing various project logs and data files. However, a previous poorly-written script created recursive symlinks in the log directories that cause infinite loops if traversed blindly.

Your goal is to write a Python script that catalogs the files without falling into infinite symlink loops, and extracts specific metadata based on the file type.

Here are the requirements:

1. **Configuration Parsing:** Read the JSON configuration file located at `/home/user/projects/config.json`. This file contains an array of projects, each with a `name` and a `log_dir`.
2. **Directory Traversal:** For each project, traverse its `log_dir` to find all files. You must explicitly avoid following any symlinks to prevent infinite loops. Do not include directories or symlinks in your final output.
3. **Data Extraction:**
   - If the file is a text log (ends with `.log`), it contains multi-line records. Read and extract only the first line (the header record), stripping any trailing newline characters.
   - If the file is a binary file (ends with `.dat`), read exactly the first 4 bytes (the magic number) and convert it to an uppercase hexadecimal string (e.g., `1A2B3C4D`).
4. **Report Generation:** Consolidate this information into a CSV file located at `/home/user/backup_report.csv`.
   - The CSV must have the following exact headers: `project_name,file_name,file_type,header_info`
   - `file_type` should be exactly `text` for `.log` files and `binary` for `.dat` files.
   - Sort the CSV rows alphabetically by `project_name` (ascending), and then by `file_name` (ascending).

Write and execute the Python script to produce `/home/user/backup_report.csv`.
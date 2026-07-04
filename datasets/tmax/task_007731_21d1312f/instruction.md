You are an AI assistant helping a developer organize a messy collection of project metadata files.

I have an archive located at `/home/user/data.tar.gz`. It contains a deeply nested directory structure with project metadata files in three formats: JSON (`.json`), XML (`.xml`), and CSV (`.csv`).

Your task is to write and execute a Bash script at `/home/user/organize.sh` that does the following:
1. Extracts `/home/user/data.tar.gz` into the directory `/home/user/raw_data`.
2. Recursively traverses `/home/user/raw_data` to find all `.json`, `.xml`, and `.csv` files.
3. Parses the project name from each file:
   - For `.json` files, extract the value of the `project_name` key at the root level.
   - For `.xml` files, extract the text content inside the `<project_name>` tag (assume it appears exactly once per file and is a simple text node).
   - For `.csv` files, the first line is always the header, which includes a `project_name` column. Extract the project name from the corresponding column in the second line (assume there is only one data row per CSV).
4. Creates a reorganized directory structure under `/home/user/organized/` based on the file extension and project name. Specifically, for each file, create a symbolic link at `/home/user/organized/<extension_without_dot>/<project_name>_<original_filename>` pointing to the absolute path of the extracted file in `/home/user/raw_data`. Spaces in project names should be replaced with underscores (`_`).
5. Generates a summary report at `/home/user/summary.txt` that lists each unique project name (with spaces replaced by underscores) and the total number of files associated with it across all formats. The report must be formatted as `<project_name>: <count>` and sorted alphabetically by project name.

You can use standard Linux tools like `jq`, `xmllint`, `awk`, `grep`, `tar`, etc., to accomplish this. Do not forget to make the script executable and run it!
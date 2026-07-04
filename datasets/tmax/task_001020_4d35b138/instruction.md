I need you to help me organize and clean up an old project backup that has been packaged in a deeply nested archive structure.

The main backup file is located at `/home/user/project_backup.tar.gz`. Inside this archive, there are project files as well as other nested archives (both `.zip` and `.tar.gz` formats) that contain more project files.

Please perform the following steps:
1. Recursively extract `/home/user/project_backup.tar.gz` and all nested archives it contains into a new directory `/home/user/extracted_project`. Ensure that no nested archives remain packed (delete the nested archive files after extracting them so only the raw project files remain).
2. Recursively traverse the `/home/user/extracted_project` directory to find all Python (`.py`) files.
3. In all `.py` files found, transform the text by replacing every instance of the exact string `FIXME:` with `TODO:`.
4. Create a single, non-nested compressed archive of the entire cleaned `/home/user/extracted_project` directory. Save this new archive as `/home/user/clean_project.tar.bz2`.
5. Finally, write a Python script (or use bash) to generate a JSON report at `/home/user/todo_report.json`. This JSON file should be a dictionary mapping the basename of each `.py` file to the total integer count of `TODO:` occurrences it contains after your text transformation.

Ensure all outputs exactly match these paths and requirements.
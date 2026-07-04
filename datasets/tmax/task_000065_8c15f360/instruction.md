You are an AI assistant helping a technical writer organize a messy archive of legacy documentation.

You have been given a compressed archive at `/home/user/legacy_docs.tar.gz`. 
This archive contains a directory structure with several text files. However, the archive is messy:
1. It contains symlinks, some of which form infinite directory loops (e.g., a link inside a subdirectory pointing back to its parent).
2. The text files are written in a mix of different character encodings (some are `utf-8`, others are `iso-8859-1`).
3. The documents reference our old company name, "AcmeCorp", which needs to be updated.

Your task is to write and execute a Python script to migrate these documents cleanly.

Perform the following steps:
1. Extract `/home/user/legacy_docs.tar.gz` into `/home/user/raw_docs/`.
2. Write a Python script to traverse the extracted directory hierarchy.
3. Your script must detect and skip any symbolic links that point to directories to avoid infinite loops. Do not copy or traverse directory symlinks.
4. For every regular file encountered, read its contents. You will need to handle the fact that files may be either `utf-8` or `iso-8859-1` encoded.
5. Convert the text to `utf-8` and replace all occurrences of the exact string `AcmeCorp` with `GlobalTech`.
6. Write the cleaned, `utf-8` encoded files into a new directory: `/home/user/clean_docs/`. The original directory structure (excluding skipped directory symlinks) must be preserved.
7. Create a log file at `/home/user/migration.log`. For every file successfully processed and written to `clean_docs`, append a line to the log in this exact format:
   `[relative_path] - [original_encoding]`
   (Example: `docs/guide.txt - iso-8859-1`). Sort the lines in the log file alphabetically by the relative path.

Ensure your Python script handles the symlinks gracefully without crashing or getting stuck in an infinite loop.
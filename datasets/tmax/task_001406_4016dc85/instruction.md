You are tasked with organizing and backing up a cluttered project repository located at `/app/messy_project`. 

A previous developer left instructions on how to process these files, but they only left it as a screenshot located at `/app/instructions.png`.

Please perform the following workflow:
1. Extract the text from `/app/instructions.png` to determine the target file extension, the target string to find, and the replacement string.
2. Search through `/app/messy_project` and its subdirectories to find all files matching the target extension that contain the target string.
3. Perform a large-scale text edit on the identified files to replace the target string with the replacement string. You must use an atomic write approach (e.g., write to a temporary file, then move/rename it over the original) to ensure data integrity during the replacement.
4. Generate a JSON manifest file at `/app/manifest.json` containing the relative paths (from `/app/messy_project/`) and the new `SHA256` checksums of ONLY the files you modified. Format the JSON as a dictionary mapping relative paths to checksum strings.
5. Create a differential backup archive at `/app/diff_backup.tar.gz` that contains ONLY the files you modified, maintaining their directory structure relative to `/app/messy_project`. 

Ensure your differential backup archive is as small as possible. The automated system will evaluate the size of `/app/diff_backup.tar.gz` as a numerical metric to ensure you didn't accidentally back up unmodified files.

Use Python or bash utilities as needed. Tesseract is available for OCR.
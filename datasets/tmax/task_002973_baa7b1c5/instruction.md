You are an AI assistant helping a technical writer organize and format a new batch of documentation. 

You have been provided with an archive located at `/app/docs_update.zip`. Warning: This archive was created by a faulty automated system and contains "zip slip" paths (e.g., `../../file.txt`) that attempt to overwrite files outside the extraction directory.

Your tasks are as follows:
1. Safely extract the contents of `/app/docs_update.zip` into the directory `/home/user/docs_clean`. You must ensure that no files are extracted outside of this directory. For entries with directory traversal paths, strip the dangerous parts (e.g., extract `../../notes.txt` as `/home/user/docs_clean/notes.txt`).
2. There is an image file at `/app/instructions.png`. Read the text from this image (you can use `tesseract`). It contains specific rules for renaming files and transforming text contents.
3. Several files in the archive are missing their file extensions. Use binary header extraction/magic bytes to identify which files are actually PNG images, and append the `.png` extension to their current filenames.
4. Apply the instructions found in `/app/instructions.png`. First, perform the text replacements in all extracted text/markdown files. Then, perform the bulk file renaming for all files in `/home/user/docs_clean` (including the PNGs you just identified).
5. Ensure all final files reside exactly in `/home/user/docs_clean`.

Your final output will be graded by an automated scoring script that checks the directory contents, file names, and text replacements. You must achieve a score of 1.0.
As a technical writer for a CNC manufacturing company, I am organizing our legacy documentation. We have an archive of old GCode files, and I need to extract all the human-readable comments from them to compile a new technical manual.

The archive is located at `/home/user/cnc_docs`. However, a previous backup script created several symlinks within this directory that form infinite loops. 

Please write and execute a Python script at `/home/user/extract.py` that does the following:
1. Recursively traverses `/home/user/cnc_docs` to find all files ending in `.gcode`.
2. Follows symlinks during traversal, but correctly detects and avoids infinite symlink loops.
3. Reads each `.gcode` file. These legacy files are encoded in `Windows-1252`.
4. Parses the files to extract all comment lines. A comment line is defined as any line where the first non-whitespace character is a semicolon (`;`).
5. Extracts the text *after* the semicolon, stripping any leading and trailing whitespace.
6. Sorts all extracted comments alphabetically.
7. Writes the sorted comments, one per line, to `/home/user/extracted_comments.txt` using `UTF-8` encoding.
8. Ensures the final write is atomic (i.e., write to a temporary file first, then atomically rename/replace it to `/home/user/extracted_comments.txt`) to prevent corrupted partial writes in case of an error.

Run your script to produce the final `/home/user/extracted_comments.txt` file.
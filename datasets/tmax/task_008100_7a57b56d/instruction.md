You are an AI assistant helping a technical writer clean up and modernize a large, messy documentation archive. 

You have been provided with a legacy documentation archive located at `/home/user/legacy_docs.tar.gz`. 

This archive has a few problems:
1. It contains a recursive symlink structure that has caused previous backup scripts to crash by following infinite loops.
2. The file extensions and naming conventions are outdated.
3. The internal macro syntax used in the text files needs to be updated.

Your task is to write a Python script at `/home/user/process_docs.py` and execute it to perform the following cleanup steps:

1. **Safe Extraction & Traversal:** 
   Extract `/home/user/legacy_docs.tar.gz` to the directory `/home/user/extracted_docs/`. Your Python script must then traverse this extracted directory. Be careful to handle or ignore symlinks so your script does not get caught in an infinite loop. Delete any symlinks you find during traversal.

2. **Bulk Renaming:**
   Find all files with the `.DOC` extension. Rename them to have a `.md` extension. Additionally, ensure the base filenames are entirely lowercase and replace any space characters (` `) with underscores (`_`). For example, `User Manual.DOC` should become `user_manual.md`.

3. **Macro Application / Text Editing:**
   Read every newly renamed `.md` file. You must perform a large-scale text edit: find all occurrences of the exact string `<macro: old_version>` and replace it with `**[Deprecated Version]**`. 

4. **Compression:**
   Once all files are renamed, edited, and the infinite symlinks are removed, compress the `/home/user/extracted_docs/` directory into a new ZIP archive located at `/home/user/clean_docs.zip`.

5. **Reporting:**
   Create a report file at `/home/user/cleanup_report.txt` containing a single integer representing the total number of `.md` files successfully processed and zipped.

Ensure you complete all steps and that `/home/user/clean_docs.zip` and `/home/user/cleanup_report.txt` are generated correctly.
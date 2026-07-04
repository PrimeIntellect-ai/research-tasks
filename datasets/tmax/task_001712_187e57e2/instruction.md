You are an AI assistant helping a technical writer consolidate project documentation. 

The writer has an old nested archive located at `/home/user/docs.tar.gz`. Inside this gzipped tarball is a single file named `project.zip`. Inside that zip file are several text files containing documentation snippets. 

Your task is to write a Python script at `/home/user/build_docs.py` that accomplishes the following:
1. **Nested Archive & Compressed Stream Processing:** The script must read `/home/user/docs.tar.gz`, extract the `project.zip` file as an in-memory stream, and read the contents of the zip file *without* extracting anything to the disk.
2. **Path Manipulation:** Search through the in-memory zip archive for all files ending with `.txt`. 
3. **Consolidation:** Read the text from these `.txt` files, decode them as UTF-8, and concatenate their contents in alphabetical order based on their file paths within the zip archive. Separate the content of each file with a single newline character `\n`.
4. **Atomic Writes:** Safely write the concatenated output to `/home/user/final_doc.md`. To prevent file corruption in case of failure, you must perform an atomic write. Write the output to a temporary file first, and then atomically move/rename it to `/home/user/final_doc.md`.
5. **Standard Streams:** The script should print the exact total number of concatenated characters (length of the final string) to `stdout`.

After writing the script, execute it in the terminal and redirect its standard output to a file named `/home/user/char_count.txt`.

Ensure your script handles the nested streams efficiently.
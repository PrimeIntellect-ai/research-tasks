You are helping a technical writer consolidate and archive a set of legacy documentation files. 

The writer has a directory of documentation files at `/home/user/docs/`. These files are currently encoded in `windows-1252`. 
You need to create a solution that safely compiles these files into a single master document while simultaneously generating a custom-compressed archive stream. Because the master document might be accessed by other background processes concurrently, you must use file locking.

Please perform the following steps:

1. Write a Python script at `/home/user/encoder.py`. 
   - The script should read file paths from standard input (one path per line).
   - For each file, it must read the contents using the `windows-1252` encoding.
   - It must acquire an exclusive file lock (using `fcntl.flock`) on the file `/home/user/compiled_docs.txt`, append the converted `utf-8` text to it, and then release the lock. (Create the file if it doesn't exist).
   - After appending to the master document, the script must "compress" the `utf-8` text using a custom algorithm: first, reverse the entire string of the file's content, and then encode the reversed string in standard Base64.
   - The script should print the Base64 "compressed" string for each file to standard output, separated by a newline.

2. Write a Bash script at `/home/user/process_docs.sh`.
   - The script should find all `.txt` files in `/home/user/docs/`, sort their paths alphabetically, and pipe the paths into `/home/user/encoder.py`.
   - It must redirect the standard output of the Python script to `/home/user/compressed_archive.b64`.

3. Execute your Bash script to process the documents.

Ensure that `/home/user/compiled_docs.txt` contains the combined UTF-8 text of all files in alphabetical order, and `/home/user/compressed_archive.b64` contains the custom compressed output.
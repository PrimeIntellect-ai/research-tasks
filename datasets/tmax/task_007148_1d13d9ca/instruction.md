I need help organizing and generating a backup manifest for a messy project directory. I tried writing a script to do this before, but it kept following symlinks into infinite loops and crashing. 

Here is what I need you to do:

1. **Clean the Configuration File**:
   I have a raw configuration file located at `/home/user/config.raw` that dictates what should be included in the backup. It's messy. Write a shell script (using `sed`, `awk`, etc.) saved at `/home/user/prep_config.sh` that cleans it up and outputs it to `/home/user/clean_config.txt`. 
   The cleaning rules are:
   - Remove any lines that start with `#` (ignoring leading whitespace).
   - Remove any blank or entirely whitespace lines.
   - Condense multiple spaces/tabs between words into a single space.
   - Remove leading and trailing whitespace on each line.

2. **Write the C Manifest Generator**:
   Write a C program at `/home/user/build_manifest.c` that reads the `/home/user/clean_config.txt` file and generates a file manifest.
   The `clean_config.txt` will have lines like:
   `INCLUDE <absolute_directory_path>`
   `EXCLUDE <file_extension>`
   
   Your C program must:
   - Parse the cleaned config to get the list of directories to include and extensions to exclude.
   - Recursively traverse every `INCLUDE` directory.
   - **Crucially**: Completely ignore any symlinks (to avoid infinite loops). Only process regular files.
   - Skip any regular files that end with any of the `EXCLUDE` extensions (e.g., if config has `EXCLUDE .tmp`, skip `file.tmp`).
   - For every valid regular file found, compute its SHA256 checksum (you may use `popen` with the `sha256sum` utility to compute this).
   - Write the results to `/home/user/manifest.txt` in the following exact format:
     `[SHA256_HASH] [ABSOLUTE_FILE_PATH]`
   - The final `/home/user/manifest.txt` must be sorted alphabetically by the absolute file path. You can sort this within your C program or by shelling out to the `sort` command at the end of your program.

Compile your program to `/home/user/build_manifest` and run it so that `/home/user/manifest.txt` is generated. 

Please ensure all paths are absolute and the final manifest is perfectly formatted.
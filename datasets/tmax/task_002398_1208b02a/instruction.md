I need you to help organize and parse some incoming binary project files. I have a staging directory with some raw binary data files, and I need an automated way to parse these files as they arrive in an `incoming` directory, appending their extracted contents to a master log.

Please do the following:

1. **Write a C program** at `/home/user/parser.c` that parses a custom binary format using **memory-mapped I/O (`mmap`)**. 
   The binary files consist of one or more contiguous records with the following structure:
   - **Magic Header**: 4 bytes, ASCII string `"DATA"`
   - **Timestamp**: 4 bytes, unsigned 32-bit integer (little-endian)
   - **Payload Length**: 2 bytes, unsigned 16-bit integer (little-endian)
   - **Payload**: Variable length ASCII string (length specified by Payload Length)
   
   The C program must take a single file path as a command-line argument. For each record in the file, it must print to standard output exactly in this format:
   `[<Timestamp>] <Payload>\n`
   Compile this program to an executable named `/home/user/parser`.

2. **Write a Bash script** at `/home/user/organize.sh` that acts as a file watcher.
   The script should loop infinitely, pausing for 1 second each iteration. During each iteration, it should check the directory `/home/user/incoming` for any files. For every file found, it should:
   - Run the compiled `./parser` executable on the file.
   - Append the output to `/home/user/project_log.txt`.
   - Delete the processed binary file.

3. **Execute the workflow**:
   - Create the directory `/home/user/incoming` if it doesn't exist.
   - Start your `organize.sh` script in the background.
   - I have pre-populated `/home/user/staging` with three files: `fileA.bin`, `fileB.bin`, and `fileC.bin`. Move all files from `/home/user/staging` into `/home/user/incoming`.
   - Wait a few seconds for your background watcher script to process them and populate `/home/user/project_log.txt`.

Your final output will be verified by checking the contents of `/home/user/project_log.txt`. Ensure all files are processed and parsed correctly.
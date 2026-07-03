You are helping a developer organize a cluttered project repository. There is a directory called `/home/user/project/dump/` containing several binary files that have lost their extensions. 

You must write a C program that classifies and helps organize these files based on their magic bytes (the first 4 bytes of the file), driven by a configuration file.

Here are the requirements:
1. Create a C program at `/home/user/project/organizer.c`.
2. The program must accept exactly one command-line argument: the path to a configuration file.
3. The configuration file is located at `/home/user/project/magic.conf`. Each line contains a 8-character hex string (representing 4 bytes) and a target directory name, separated by a colon (e.g., `89504e47:textures`). Note that the hex string in the config file will be lowercase.
4. The C program must read file paths from standard input (`stdin`), one path per line.
5. For each file path read from standard input, the program must:
   - Open the file in binary mode.
   - Read the first 4 bytes.
   - Compare the hex representation of these 4 bytes (in lowercase) against the entries loaded from the configuration file.
   - If a match is found, output a shell command to standard output (`stdout`) in the exact following format:
     `mv '<FILE_PATH>' '/home/user/project/organized/<TARGET_DIR>/'`
     (Ensure you include the single quotes around paths to handle potential spaces, though our test files won't have spaces).
   - If a file does not match any magic bytes in the config, it should be ignored (no output).
6. Compile your program to `/home/user/project/organizer`.
7. Ensure the target directories exist inside `/home/user/project/organized/` (create them using shell commands based on the config file targets: `textures`, `objects`, `archives`).
8. Execute your compiled program by piping the list of files in `/home/user/project/dump/` into it, and then pipe the output directly into `bash` to perform the actual moves. For example:
   `ls -1 /home/user/project/dump/* | ./organizer /home/user/project/magic.conf | bash`

Verify your success by checking that the files from the dump directory have been moved into the correct subdirectories inside `/home/user/project/organized/`.
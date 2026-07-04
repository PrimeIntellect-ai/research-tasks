You are acting as a backup administrator. We need to archive a set of actively written log files, but before doing so, we must generate a manifest with checksums for all valid logs. 

Your task is to implement a fast, reliable backup manifest generator pipeline in C++ and Bash.

Follow these exact steps:

1. **Write a C++ program**: Create `/home/user/checksum_gen.cpp` and compile it to `/home/user/checksum_gen`. 
   - The program must read file paths line-by-line from Standard Input (`stdin`).
   - For each file, open it and calculate a simple checksum: the sum of the ASCII values of all characters in the file, modulo 256.
   - For each file, print to Standard Output (`stdout`) exactly: `<filepath> <checksum>` (separated by a single space), followed by a newline.
   - Ignore any files that cannot be opened.

2. **Write a Bash script**: Create `/home/user/backup.sh`.
   - The script must use `find` to search the directory `/home/user/active_logs/`.
   - It should ONLY select files that have the `.log` extension AND are strictly larger than 10 bytes in size.
   - It must pipe the list of found files into the `/home/user/checksum_gen` program.
   - The output of the C++ program must be redirected into the file `/home/user/backup_manifest.txt`.
   - Sort the final output in `/home/user/backup_manifest.txt` alphabetically by filepath. You can do this by piping the C++ output through `sort` before writing to the file.

3. **Execute**: Run your `backup.sh` script so that `/home/user/backup_manifest.txt` is created with the correct data.

Assume the `/home/user/active_logs/` directory already exists and is populated with logs. Make sure all scripts and source files are saved in `/home/user/`.
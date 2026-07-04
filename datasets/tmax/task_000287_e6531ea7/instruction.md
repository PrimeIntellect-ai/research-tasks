You are assisting a technical writer in organizing a chaotic dump of legacy engineering documentation and manufacturing files. The files are currently trapped in a deeply nested archive, are missing proper file extensions, and need to be categorized, parsed, and indexed for a new documentation system.

Your objective is to complete the following multi-phase process using strictly Bash and standard Linux utilities:

**Phase 1: Nested Archive Extraction**
An archive is located at `/home/user/incoming/legacy_dump.tar.gz`. Extract it into `/home/user/extracted/`. However, this archive contains other archives (`.tar`, `.tar.gz`, `.zip`) inside it, sometimes multiple levels deep. Write a command or short script to recursively unpack all nested archives within `/home/user/extracted/` until no archive files remain. Delete the intermediate archive files after extracting them.

**Phase 2: Binary Header Extraction & Organization**
Due to system corruption, many files have lost their extensions. 
1. Create the directory `/home/user/organized/bin/`.
2. Inspect every file in `/home/user/extracted/` (and its subdirectories). Identify all compiled ELF executables strictly by checking their "magic bytes" (the first 4 bytes of an ELF file are always `\x7fELF`).
3. Move all identified ELF files into `/home/user/organized/bin/`.

**Phase 3: Domain-Specific Parsing (GCode)**
The dump contains several 3D printing GCode files.
1. Identify all GCode files in the extracted folders (they all contain the string `; FLAVOR:Marlin` in their first 10 lines).
2. From each identified GCode file, extract the estimated printing time, which is written in a comment like this: `; TIME:4521` (where 4521 is the time in seconds).
3. Create a report at `/home/user/organized/gcode_times.txt`. Each line must be formatted exactly as: `[basename_of_file]: [time_in_seconds]s`. Sort this file alphabetically by filename.

**Phase 4: File Splitting**
Find any `.log` files in the extracted directories. Split any `.log` file into chunks of exactly 500 lines. Name the split files in the same directory using the format `[original_basename]_part_aa.log`, `[original_basename]_part_ab.log`, etc. Delete the original `.log` files after splitting.

**Phase 5: Concurrent Indexing Script**
Write a bash script at `/home/user/build_index.sh` that processes all plain text files remaining in `/home/user/extracted/` (including the newly split logs). 
The script must:
1. Loop through all text files and read their first line.
2. Launch a background job (`&`) for each file to process them concurrently.
3. Each background job must append the data to `/home/user/organized/master_index.txt` in the format: `[basename_of_file] | [first_line]`.
4. Because multiple background jobs will write to `master_index.txt` simultaneously, you **must** use `flock` to acquire an exclusive lock on the file during the append operation to prevent data corruption.
5. Wait for all background jobs to finish.

Run your `/home/user/build_index.sh` script to generate the final `master_index.txt`.

Ensure all operations are completed and the final files are precisely where requested.
You are tasked with organizing a legacy C++ project that has been handed over from an international team. The project files are currently archived, poorly named, and encoded in ISO-8859-1. You need to extract them, set up an incremental backup system, parse an index file to rename the source files, and convert their contents to UTF-8 using a custom C++ program.

Perform the following steps exactly as described:

1. **Extraction & Baseline Backup:**
   - Extract the archive located at `/home/user/legacy_data.tar.gz` into a new directory `/home/user/project/`.
   - Create a full tarball backup of the `/home/user/project/` directory at `/home/user/backup_full.tar.gz`. Crucially, you must use GNU `tar`'s listed-incremental backup feature, saving the snapshot metadata to `/home/user/backup.snar`.

2. **C++ Processing Program:**
   - Write a C++ program at `/home/user/process.cpp` and compile it to `/home/user/process` (using standard C++17, no external libraries).
   - The `/home/user/project/` directory contains an `index.csv` file with the format: `old_filename,new_filename`.
   - Your C++ program must parse `index.csv`. For each file listed:
     a. Read the contents of `old_filename` (which is encoded in ISO-8859-1).
     b. Convert the ISO-8859-1 text to UTF-8 encoding in memory. (Hint: ISO-8859-1 maps exactly to the first 256 Unicode code points).
     c. Write the UTF-8 converted text to `new_filename` in the `/home/user/project/` directory.
     d. Delete the `old_filename` from the filesystem.
   - Run your compiled `/home/user/process` executable from within the `/home/user/project/` directory.

3. **Incremental Backup & Logging:**
   - After the C++ program finishes processing, create an incremental backup of the modified `/home/user/project/` directory at `/home/user/backup_inc.tar.gz`. Use the same `/home/user/backup.snar` snapshot file so that only the new/modified files and directory changes are captured.
   - Finally, create a log file at `/home/user/completion.log` containing the final list of files inside `/home/user/project/` (just the basenames, one per line, sorted alphabetically).

Ensure all created backup files, executables, and the final source files exist exactly at the paths specified.
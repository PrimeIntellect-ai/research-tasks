You are acting as a backup administrator managing legacy data archives. We have a batch of old files extracted from a legacy storage system into a temporary directory: `/home/user/legacy_archive`.

Because these files came from an older system, their filenames are encoded in **ISO-8859-1** (Latin-1), not standard UTF-8. Furthermore, their file extensions are currently in uppercase, which violates our modern archiving standards.

Your task is to write a C++ program that normalizes these filenames. 

Create a C++ program at `/home/user/normalize.cpp` that does the following:
1. Iterates over all files in the directory `/home/user/legacy_archive`.
2. Reads the current filename and converts its character encoding from ISO-8859-1 to standard UTF-8.
3. Manipulates the path to convert the file extension (everything after the last dot) to strictly lowercase. If the file has no extension, leave it as is.
4. Performs a bulk rename of the files in the directory to their new UTF-8, lowercase-extension names.
5. Writes a log of the renaming operations to `/home/user/normalization.log`.

**Log Format Constraints:**
For every file processed, write a single line to the log file in the exact following format:
`[ABSOLUTE_OLD_PATH] -> [ABSOLUTE_NEW_PATH]`

Example log entry:
`/home/user/legacy_archive/photo.JPG -> /home/user/legacy_archive/photo.jpg`

*Note: You are guaranteed that the original filenames only contain valid ISO-8859-1 bytes. You may use standard C++17 filesystem libraries (`<filesystem>`). Ensure your program compiles successfully with `g++ -std=c++17`.*

Compile your program to `/home/user/normalize` and execute it to process the directory.
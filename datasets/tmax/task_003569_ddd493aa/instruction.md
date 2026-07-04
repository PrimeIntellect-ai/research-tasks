I am organizing a messy directory of project files located at `/home/user/project_files`. During a previous sync, many file extensions were lost or altered. I know there are several ZIP and GZIP archives hidden among the regular text and data files.

Please write a Go program at `/home/user/detect.go` that does the following:
1. Recursively traverses the `/home/user/project_files` directory.
2. Opens each file and reads its binary header (the first few bytes) to determine if it is an archive.
3. Specifically, detect files that start with the ZIP magic number (`50 4B 03 04` in hex) or the GZIP magic number (`1F 8B 08` in hex).
4. Prints the absolute path of every detected archive file to standard output, one path per line.

Once you have written the Go program, run it, sort its output alphabetically, and pipe the final sorted output into a file at `/home/user/found_archives.txt`.

Do not hardcode the expected files in your Go program; it must dynamically inspect the file headers. Ignore directories and files that cannot be read, but you must correctly identify the disguised archives based strictly on their binary signatures.
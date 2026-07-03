You are an artifact manager curating a binary repository. You have received a new update archive located at `/home/user/artifacts/update.tar`.

Recently, several archives have been discovered to contain path traversal vulnerabilities (often known as "Zip Slip" or "Tar Slip"). Malicious actors create archives with files that use absolute paths or relative paths with `../` to overwrite critical system files when extracted.

Before extracting any files, you must verify the archive's integrity by inspecting its contents and safely transforming the file names for the next pipeline stage.

Perform the following tasks:
1. Write a C program at `/home/user/filter.c` that reads lines from standard input (stdin). For every line read, it should print the line to standard output (stdout) UNLESS the line starts with a forward slash (`/`) or contains the exact substring `../`. 
2. Compile this C program to `/home/user/filter`.
3. List the contents of the archive `/home/user/artifacts/update.tar` using the appropriate `tar` command.
4. Pipe the output of the `tar` listing through your compiled `/home/user/filter` program.
5. Pipe the output of the filter into a stream editor (`sed` or `awk`) to rename the extension of any object files. specifically, replace any `.o` extension at the end of a line with `.obj`.
6. Redirect the final output into a log file located at `/home/user/verified_artifacts.log`.

Do not extract the archive. The final `/home/user/verified_artifacts.log` should only contain the safe paths, one per line, with the object file extensions properly transformed.
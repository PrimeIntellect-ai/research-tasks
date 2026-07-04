I am working on a custom configuration manager that tracks file changes by bundling them into a custom archive format. I need you to write a C program that archives a directory, handles symbolic links safely without following them (to avoid infinite loops), and applies a custom basic compression.

There is a directory structure at `/home/user/configs` which contains configuration files, directories, and some circular symlinks that have caused standard naive scripts to loop infinitely.

Please write a C program at `/home/user/archiver.c` that does the following:
1. Recursively traverses the directory given as the first command-line argument.
2. For every directory encountered, writes a line to standard output in the format: `DIR|<relative_path>`
3. For every symbolic link encountered (do NOT follow it), writes to standard output: `LINK|<relative_path>|<symlink_target_string>`
4. For every regular file encountered, reads its contents, compresses it using Run-Length Encoding (RLE), and writes to standard output: `FILE|<relative_path>|<compressed_length>|<compressed_content>`
5. Any relative paths should start from the root of the provided directory. For example, if traversing `/home/user/configs`, the path `/home/user/configs/app.conf` should be represented simply as `app.conf`. The root directory itself should not be output as a `DIR|` entry.

**RLE Compression Specification**:
For regular files, encode consecutive identical characters as the decimal count of occurrences followed by the character. For example, the string `aaaabbbcc\n` becomes `4a3b2c1\n`. Every character (including newlines and spaces) must be encoded this way.

Compile your program to `/home/user/archiver`.
Then, run your program with `/home/user/configs` as the argument, and redirect its standard output to create the archive at `/home/user/backup.archive`.

Make sure your program properly uses `lstat` instead of `stat` to detect the symlinks and avoid falling into an infinite loop caused by the circular links in the `configs` directory. The order of entries in the archive does not matter, but all files, directories, and links within `/home/user/configs` must be present.
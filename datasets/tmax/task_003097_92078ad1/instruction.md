You are tasked with building a custom configuration tracking and incremental backup utility using Rust. 

As a configuration manager, you need to track changes between a backup of a configuration directory and its current state. To save space, any changed files must be backed up using a custom Run-Length Encoding (RLE) compression algorithm.

You must write a Rust program located at `/home/user/tracker.rs` and compile it to `/home/user/tracker`.

The program must meet the following specifications:
1. It accepts exactly two arguments: a base directory and a target directory (e.g., `./tracker /home/user/etc_backup /home/user/etc_mock`).
2. It navigates the target directory. For every file in the target directory, it checks if the file exists in the base directory and has the exact same contents. 
3. If the file is new or modified (its content differs from the base directory), the program must output the file's relative path (relative to the target directory) and its RLE-compressed content to standard output. If the file is unchanged, it outputs nothing for that file.
4. The custom RLE compression must encode the file's contents (which are guaranteed to be ASCII text) by counting consecutive occurrences of the same character. The format for each run is the count (as a base-10 integer) followed immediately by the character itself. For example, the text `AAABBB` becomes `3A3B`. A single newline character `\n` would become `1\n`.
5. The output format for each modified or new file must be exactly:
```
FILE: <relative_path>
<RLE_compressed_content>
```
(No trailing newline after the RLE content, except what is encoded from the file itself, but append a newline after the compressed block to separate files if you wish. Specifically, ensure the output format exactly matches standard consecutive printing). 
Wait, to be precise, print `FILE: <relative_path>\n` followed by `<RLE_compressed_content>\n`.

After writing and compiling the program, run it to compare `/home/user/etc_backup` (base) and `/home/user/etc_mock` (target). 
Redirect the standard output of your program to `/home/user/config_diff.out`.

Ensure that your Rust program handles basic path manipulations securely and relies on standard stream redirection for the final output.
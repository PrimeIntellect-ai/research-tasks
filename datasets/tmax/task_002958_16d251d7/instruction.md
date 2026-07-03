You are helping a researcher organize a massive scientific dataset. The researcher has a custom file-system journal format that records dataset operations (bulk file renaming, hard link creation, and symlink management). These journals are massive, so they are always compressed using `bzip2`. 

Your goal is to write a fast C++ utility named `/home/user/journal_compiler` that reads a `bzip2`-compressed binary journal from `stdin`, uncompresses it on the fly, and writes the equivalent bash script to `stdout`.

We have provided the `bzip2-1.0.8` source code at `/app/bzip2-1.0.8`. The researcher tried to build it to link against it, but the `make` command fails immediately due to a configuration error in the vendor's source directory. 

Here are your steps:
1. Fix the build issue in `/app/bzip2-1.0.8` and compile the static library (`libbz2.a`).
2. Write a C++ program at `/home/user/journal_compiler.cpp`.
3. Compile your program to `/home/user/journal_compiler`, statically linking against the `libbz2.a` you just built.
4. Your program must read a `bzip2` stream from standard input (`stdin`) until EOF.
5. As it decompresses the stream, it must parse the binary journal and output standard shell commands to standard output (`stdout`), followed by a newline for each command.

**Binary Journal Format (Uncompressed)**
The stream is a sequence of entries. Each entry starts with a 1-byte Opcode.

*   **Opcode `0x00` (Bulk Rename):** 
    *   Followed by a 2-byte unsigned integer `N` (little-endian), representing the number of files to rename.
    *   Followed by `N` pairs of null-terminated strings (`old_name` then `new_name`).
    *   **Output:** For each pair, print `mv '<old_name>' '<new_name>'`.
*   **Opcode `0x01` (Hard Link):**
    *   Followed by two null-terminated strings (`target` then `link_name`).
    *   **Output:** Print `ln '<target>' '<link_name>'`.
*   **Opcode `0x02` (Symbolic Link):**
    *   Followed by two null-terminated strings (`target` then `link_name`).
    *   **Output:** Print `ln -s '<target>' '<link_name>'`.

*Note: You must properly escape single quotes inside the string variables if any exist, by replacing `'` with `'\''`. However, you can assume for simplicity that the input strings will only contain alphanumeric characters, underscores, dots, and hyphens.*

Ensure your compiled executable is located at `/home/user/journal_compiler`. Our automated tests will pipe numerous heavily-compressed randomized journals into your executable and verify that the output perfectly matches the reference implementation.
You are a developer organizing project text files into a custom archive format. You need to write a C program that applies a custom Run-Length Encoding (RLE) compression to the contents of files and outputs the combined archive.

Write a C program at `/home/user/archiver.c` that does the following:
1. Reads file paths from standard input, one per line (up to 256 characters per line).
2. For each file path read:
   - Prints a header line exactly formatted as: `---[BASENAME]---` followed by a newline. For example, if the path is `/home/user/project/sub/doc.txt`, the header is `---doc.txt---`.
   - Reads the contents of the file.
   - Applies a custom RLE compression to the contents: for every sequence of identical consecutive characters, output the character followed immediately by the count of its occurrences as an integer (e.g., "AAAABBBCC" becomes "A4B3C2"). This applies to all characters, including spaces and newlines (e.g., a single newline becomes `\n1`).
   - Prints a final newline character after the RLE string for that file.

Once your program is written and compiled to `/home/user/archiver`:
Use shell commands to recursively find all `.txt` files in `/home/user/project_files`, sort their full paths alphabetically, pipe them into your C program, and redirect the standard output to `/home/user/organized_archive.rle`.

**Notes:**
- Only use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `libgen.h`).
- Handle files with missing trailing newlines gracefully (just RLE what is there).
- The final archive must strictly match the expected RLE format.
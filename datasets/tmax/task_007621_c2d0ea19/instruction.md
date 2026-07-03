I am a technical writer trying to organize a massive documentation build log. Our documentation system outputs multi-line error records mixed in with standard build output. I need to extract only the "FATAL" documentation errors to prioritize fixing them.

Please help me by writing a C program that acts as a stream filter. 

Here are the requirements:
1. Create a C program at `/home/user/filter.c`.
2. The program must read from standard input (`stdin`) and write to standard output (`stdout`).
3. The input contains standard text and multi-line error blocks. An error block always starts with the exact line `[DOC-ERROR]` and ends with the exact line `[END-ERROR]`. 
4. The C program must extract and print the entire error block (including the `[DOC-ERROR]` and `[END-ERROR]` lines) **only** if the block contains a line that starts exactly with `Severity: FATAL`.
5. Standard text outside of these blocks, and error blocks with any other severity (like `Severity: WARN`), must be completely ignored.
6. Compile your C program to an executable named `/home/user/filter`.
7. Process the log file located at `/home/user/raw_docs.log` by redirecting or piping it through your compiled executable, and save the exact output to `/home/user/fatal_errors.log`.

Do not add any extraneous output, prefixes, or headers to the output file; it should only contain the matching blocks exactly as they appeared in the original log.
You are tasked with fixing a broken configuration tracking pipeline. 

We have a system that tracks configuration changes and exports them to a CSV file at `/home/user/config_changes.csv`. The CSV has the following columns:
`ChangeID,Service,ConfigData,Author`

The `ConfigData` column contains JSON snippets. If a JSON snippet spans multiple lines, the entire `ConfigData` field is enclosed in double quotes (`"`). Unfortunately, standard UNIX line-oriented tools (like `grep`, `awk`, or `wc`) cannot handle these embedded newlines properly. 

Your task is to:
1. Write a C program at `/home/user/sanitize.c` that reads from standard input (stdin) and writes to standard output (stdout). 
2. The C program must track whether it is currently inside double quotes. If it reads a newline character (`\n`) while *inside* double quotes, it should replace it with a single space character (` `). All other characters should be passed through unchanged. (You do not need to handle escaped quotes like `\"` or `""` for the state tracking; a simple toggle on `"` is sufficient for this dataset).
3. Compile the program to `/home/user/sanitize`.
4. Create a shell pipeline that uses your compiled C program to sanitize `/home/user/config_changes.csv`.
5. In the same pipeline, extract the `Author` field (which is always the last comma-separated field on the sanitized line), calculate the total number of changes made by each author, and save the results to `/home/user/author_stats.csv`.

The final `/home/user/author_stats.csv` must:
- Omit the CSV header row (i.e., do not include "Author" in the counts).
- Be formatted as exactly: `author_name,count` (e.g., `alice,5`).
- Be sorted alphabetically by author name.

Note: You can assume the input file is perfectly well-formed according to the simple quoting rule above.
You are a data engineer tasked with building an ETL pipeline that extracts data from a relational CSV file and a document-oriented text file, maps them into a graph representation, and queries it for a specific knowledge graph pattern.

Your environment contains two data sources in `/home/user/`:

1.  `users.csv`: A relational-style CSV containing user data.
    Format: `id,name,role`
    Example:
    ```
    u1,Alice,Engineer
    u2,Bob,Manager
    ```

2.  `docs.txt`: A document-oriented file containing metadata about documents. Each document's metadata is separated by `---`.
    Format:
    ```
    DOC: d1
    AUTHOR: u1
    CITES: d2, d5
    ---
    DOC: d2
    AUTHOR: u2
    CITES: 
    ```

Your task is to:
1.  Write a shell script `/home/user/etl.sh` that parses `docs.txt` and flattens it into a strictly relational edge-list format.
2.  Write a C program `/home/user/pattern_match.c` that reads `users.csv` and the transformed document data.
3.  The C program must build an internal graph to find instances of the following Knowledge Graph pattern:
    **An 'Engineer' wrote a document that CITES a document written by a 'Manager'.**
4.  The C program must output the matching pairs to `/home/user/matches.txt` in the format: `[Engineer_Name] cites [Manager_Name]`.
    *   Each matching pair should be printed on a new line.
    *   The output must be sorted alphabetically by the Engineer's name, then the Manager's name.
    *   If an Engineer cites multiple documents by the same Manager, output the pair only once (distinct pairs).

Requirements:
*   You must rely entirely on standard Linux coreutils (e.g., awk, sed, grep) for the bash portion, and write standard C code for the pattern matching.
*   Do not use any external C libraries (only standard library headers like `stdio.h`, `stdlib.h`, `string.h` are allowed).
*   Compile your program to `/home/user/pattern_match_exe`.
*   Ensure the final results are safely written to `/home/user/matches.txt`.
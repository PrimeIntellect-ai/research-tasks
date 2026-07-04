You are an AI assistant helping a researcher organize and cross-reference a multi-modal dataset of academic papers. The researcher has data spread across three different representations: a relational database, a graph adjacency list, and a flat document store.

Here is the current state of the dataset located in `/home/user/`:
1. `papers.db`: A SQLite3 database containing a table `papers` with columns `id` (INTEGER PRIMARY KEY), `title` (TEXT), and `author` (TEXT). This stores the core relational metadata.
2. `citations.txt`: A text file representing a citation graph in an adjacency list format. Each line contains two integers separated by a space: `cited_id citing_id`. This means the paper with `citing_id` cites the paper with `cited_id`.
3. `abstracts.txt`: A document store where each line contains a paper ID and its abstract, separated by a pipe character (`|`), formatted as `id|abstract text`.

Your task is to write a C program `/home/user/process_results.c` that compiles to an executable named `/home/user/process_results`. 

The program must take exactly one command-line argument: an author's name (e.g., `"Dr. Alice Smith"`).
When executed, the program must chain together queries across these three representations to do the following:
1. Query `papers.db` to find all `id`s of papers written by the specified author.
2. Cross-reference those IDs with the graph in `citations.txt` to find all `citing_id`s (the IDs of papers that cite the author's papers).
3. Retrieve the abstracts for those `citing_id`s from `abstracts.txt`.
4. Output the results to a file named `/home/user/report.tsv` in a tab-separated format.

The format of `/home/user/report.tsv` must be exactly:
`OriginalPaperID\tCitingPaperID\tCitingAbstract`
(where `\t` represents a literal tab character). The rows should be ordered by `OriginalPaperID` ascending, and then by `CitingPaperID` ascending.

Constraints & Allowances:
- You must write the solution primarily in C.
- You may use standard C libraries. Since you do not have root access to install `libsqlite3-dev`, you are allowed and encouraged to use `popen()` within your C program to call the `sqlite3` command-line utility to query the database and read its stdout stream.
- Compile your program using `gcc /home/user/process_results.c -o /home/user/process_results`.
- Run your program with the argument `"Dr. Alan Turing"` to generate the final `report.tsv`.
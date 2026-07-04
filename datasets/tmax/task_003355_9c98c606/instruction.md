I am a researcher organizing a graph database of academic literature. I have an SQLite database containing citation data, but I need to extract specific topological patterns (knowledge graph motifs) to identify highly collaborative sub-fields. 

The database is located at `/home/user/research_data.db` and contains two tables:
1. `papers`: `id` (INTEGER), `title` (TEXT), `year` (INTEGER)
2. `citations`: `source_id` (INTEGER), `target_id` (INTEGER) -> indicates that the paper with `source_id` cites the paper with `target_id`.

I need you to write a C++ program at `/home/user/extract_pattern.cpp` that uses the SQLite3 C API (`<sqlite3.h>`) to find all "citation triangles" (cycles of length 3) where:
- Paper A cites Paper B
- Paper B cites Paper C
- Paper C cites Paper A
- All three papers were published in the year 2020 or later.

Your C++ program must execute the appropriate SQL query (using complex joins) to find these patterns and export the results to a TSV file at `/home/user/cycles.tsv`.

Requirements for `/home/user/cycles.tsv`:
- Each line should represent one unique citation triangle.
- The format must be three integer IDs separated by single tabs (e.g., `14\t29\t33`).
- On each line, the three IDs must be sorted in strictly ascending order (ID1 < ID2 < ID3) so that equivalent cycles (e.g., A-B-C, B-C-A) are normalized to the same sequence.
- The lines themselves must be sorted lexicographically (or by ID1, then ID2, then ID3).
- Do not include column headers.

Please compile your code into an executable at `/home/user/extract_pattern` (e.g., `g++ -std=c++17 extract_pattern.cpp -lsqlite3 -o extract_pattern`) and run it so that the `/home/user/cycles.tsv` file is generated.
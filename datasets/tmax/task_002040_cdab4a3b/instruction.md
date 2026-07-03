You are a Database Reliability Engineer (DBRE) responsible for restoring Graph Database backups from an untrusted source. The backups contain embedded NoSQL JSON manifests, which include automated Cypher migration scripts to be executed upon restore. We need to prevent any malicious or destructive Cypher queries from being executed.

We have provided a proprietary C++ parsing library, `libgraphbackup`, located at `/app/libgraphbackup-1.2.0`, which extracts Cypher queries from our custom NoSQL JSON backup format. 

Your task is to:
1. **Fix the Vendored Library**: The `libgraphbackup` package is currently broken. Its `Makefile` has a misconfiguration preventing it from compiling into a shared library. Diagnose and fix the build system, then run `make` and `make install` (which will install to `/app/libgraphbackup-1.2.0/build/lib` and `/app/libgraphbackup-1.2.0/build/include`).
2. **Develop a Sanitizer Utility**: Create a C++ program at `/home/user/filter_backup.cpp` that links against `libgraphbackup`. 
   - It should accept a single command-line argument: the path to a backup JSON file.
   - It must use the library function `std::vector<std::string> extract_queries(const std::string& filepath);` (defined in `graphbackup.h`) to read the file.
   - It must scan the extracted Cypher queries for destructive operations. A query is considered "evil" (malicious) if it contains any of the following substrings (case-insensitive): `DELETE`, `DROP`, `REMOVE`, or `CALL dbms.`.
3. **Compile and Test**: Compile your program into an executable at `/home/user/filter_backup`. 
   - If a file contains ONLY safe queries, the program MUST exit with code `0`.
   - If a file contains ANY evil queries, the program MUST exit with code `1`.

We have provided a test suite of backup files in two directories:
- `/app/corpora/clean/`: Contains 50 backup files with entirely safe read/write operations (e.g., MATCH, CREATE, MERGE).
- `/app/corpora/evil/`: Contains 50 backup files containing destructive queries (e.g., DROP INDEX, DETACH DELETE).

You must ensure your `/home/user/filter_backup` executable successfully processes all files in both corpora, exiting with `0` for clean files and `1` for evil files.
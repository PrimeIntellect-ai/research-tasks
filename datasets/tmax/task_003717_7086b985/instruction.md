You are a Data Engineer building an ETL pipeline to migrate data from a legacy graph database into a modern NoSQL document store. 

We have a legacy, stripped binary located at `/app/graph_engine` which executes proprietary Cypher-like queries and outputs pipe-separated values (PSV). Unfortunately, this legacy engine has a severe bug: it contains a corrupted index (`stale_rels`). If a query forces the use of this index (e.g., via the hint `USING INDEX stale_rels`), or if an unparameterized query attempts to traverse the corrupted relationship `[:CORRUPT]`, the engine will either segfault or silently return mixed/stale rows, ruining our ETL pipeline.

Your task is to create a C program that acts as a secure query wrapper, sanitizer, and format converter. 

1. Write your C program at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
2. The program must read a single graph query from standard input (stdin).
3. **Validation (Adversarial Filter):** The program must analyze the query string. 
   - If the query contains the exact substring `USING INDEX stale_rels` OR contains the exact substring `:CORRUPT`, the program must reject the query. It must print exactly `REJECT` to standard output and exit with status code `1`.
   - If the query does not contain these malicious/corrupted patterns, it is considered safe.
4. **Execution & Export:** For safe queries, your C program must execute the `/app/graph_engine` binary as a child process, feeding the safe query to the binary's stdin.
5. **NoSQL JSON Export:** The `/app/graph_engine` outputs data in PSV format (e.g., `id|name|age\n1|Alice|30\n`). Your C program must capture this output, parse it, and convert it into a strictly formatted JSON array of objects (where the first row provides the JSON keys). Print the resulting JSON to standard output and exit with status code `0`.

Example JSON output format:
```json
[
  {"id": "1", "name": "Alice", "age": "30"}
]
```

To help you develop and test, two corpora of raw query files are provided:
- `/home/user/clean/`: Contains safe queries that must be executed and converted to JSON.
- `/home/user/evil/`: Contains queries that trigger the corrupted index, which must be rejected.

Ensure your program can correctly process all files in these directories by reading them via stdin (e.g., `./sanitizer < /home/user/clean/query1.txt`). Do not use any external C libraries outside of the standard POSIX libc.
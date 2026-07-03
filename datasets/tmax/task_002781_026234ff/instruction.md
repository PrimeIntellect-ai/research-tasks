As a Database Administrator optimizing our new analytics stack, you have been tasked with securing our legacy query execution pipeline. We have a proprietary query validator binary located at `/app/query_oracle`. This tool parses incoming SQL queries (which extensively use complex joins, window functions, and knowledge graph pattern matching) and determines if they are safe to execute.

Unfortunately, `/app/query_oracle` is a stripped binary and has a known vulnerability: it fails to detect "Cartesian Bombs" (queries using `CROSS JOIN` or implicit comma joins without a corresponding `WHERE` or `LIMIT` clause) and nested CTE recursion bombs (queries containing more than 3 levels of nested `WITH RECURSIVE` statements). These malicious queries exhaust our database resources.

Your task is to implement a robust SQL pre-filter in C.
1. Write a C program at `/home/user/filter.c`.
2. Compile it to `/home/user/filter` using `gcc`.
3. The program must read a raw SQL query from `stdin`.
4. It must output exactly `ACCEPT` (followed by a newline) if the query is safe, or `REJECT` (followed by a newline) if the query contains malicious Cartesian or recursive bomb patterns.
5. You can use `/app/query_oracle` to understand the baseline validation (it outputs `SAFE` or `UNSAFE` for standard syntax), but your C program must correctly flag the edge cases the oracle misses, while still allowing valid complex joins, window functions, and graph pattern matching queries.

Ensure your program handles standard SQL formatting (including newlines and varying whitespace). You may use standard C libraries (`stdio.h`, `string.h`, `regex.h`, etc.). The final executable must be located precisely at `/home/user/filter`.
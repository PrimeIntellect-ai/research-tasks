You are acting as a data engineer for a research lab organizing a bibliographic knowledge graph. 

We have a dataset of academic relationships stored in a CSV file at `/home/user/kg_edges.csv`. The format is `Subject,Relation,Object`.
Relations are either `WROTE` (Subject is an Author, Object is a Paper) or `AFFILIATED_WITH` (Subject is an Author, Object is an Institution).

A previous researcher wrote a C program, located at `/home/user/find_pattern.c`, to extract a specific knowledge graph pattern. The goal was to find instances where two distinct authors co-authored the *same* paper and are affiliated with the *same* institution. 
However, the current C code has a logical flaw akin to an "implicit cross join" in SQL: it finds pairs of authors at the same institution who each wrote *a* paper, but fails to ensure they wrote the *same* paper. This results in an explosion of incorrect pairs.

Your task is to fix and enhance the C program:
1.  **Fix the Graph Pattern Match:** Modify `/home/user/find_pattern.c` so it only matches pairs of authors (`A1`, `A2`) where `A1` and `A2` `WROTE` the identical paper `P`, and `A1` and `A2` are `AFFILIATED_WITH` the identical institution `I`. Ensure `A1` is strictly less than `A2` (lexicographically) to avoid duplicate reciprocal pairs.
2.  **Sort the Results:** The extracted tuples `(A1, A2, P, I)` must be sorted lexicographically in this exact priority: `P` (Paper) ascending, then `I` (Institution) ascending, then `A1` ascending, then `A2` ascending.
3.  **Pagination / Filtering:** The code must output ONLY the first 3 results (Limit 3, Offset 0) from the sorted list.
4.  **Output Schema Validation:** The program must write its output to `/home/user/output.json`. The output must be a strictly valid JSON array of objects, with keys exactly named `"A1"`, `"A2"`, `"P"`, and `"I"`. For example: `[{"A1": "Alice", "A2": "Bob", "P": "Graph Theory", "I": "MIT"}]`.

Compile your fixed C program, execute it, and ensure `/home/user/output.json` is generated with the correct schema, sorted, and paginated results. Use standard C libraries (e.g., `stdio.h`, `stdlib.h`, `string.h`).
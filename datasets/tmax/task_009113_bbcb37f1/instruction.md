You are an AI assistant helping a bioinformatics researcher organize and query a newly acquired, undocumented dataset. 

The researcher has downloaded a raw dataset file located at `/home/user/knowledge_base.tsv`. This file represents a knowledge graph in a tab-separated values (TSV) format (`Subject \t Predicate \t Object`). Unfortunately, the data dictionary was lost, so you first need to explore the file to reverse-engineer the data model (i.e., figure out what predicates are used to connect researchers, publications, and research topics).

Your objective is to build a fast C++ command-line tool that performs a specific parameterized graph pattern matching query. 

**The Query Requirement:**
Given a specific researcher (Person A) and a specific topic (Topic B), the researcher wants to find all *other* researchers (Person C) who meet BOTH of the following conditions:
1. Person C has co-authored at least one publication with Person A.
2. Person C has authored at least one publication (which could be the same or a different publication) that focuses on Topic B.

**Instructions:**
1. Inspect `/home/user/knowledge_base.tsv` to understand the graph's schema and identify the exact predicates used for "authoring a publication" and "a publication's topic". Note the directionality of the edges!
2. Write a C++ program at `/home/user/graph_query.cpp` that loads the graph into memory and efficiently executes the query pattern described above.
3. Your C++ program must accept exactly three command-line arguments in this order:
   `./graph_query <path_to_tsv> <Person_A_ID> <Topic_B_ID>`
4. The program must output the resulting "Person C" IDs to a file named `/home/user/query_results.txt`. 
   - Write one ID per line.
   - The IDs must be sorted alphabetically.
   - Do not include Person A in the output.
   - Do not include duplicates.
5. Compile your program to `/home/user/graph_query` using standard `g++` (C++17 is allowed).
6. Once compiled, run your program using `Person_1` as Person A and `Topic_X` as Topic B.

Ensure the final results are written to `/home/user/query_results.txt` and the executable exists at `/home/user/graph_query`.
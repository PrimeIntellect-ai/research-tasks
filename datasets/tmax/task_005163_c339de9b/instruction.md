You are an AI assistant helping a researcher organize and process a dataset of scientific publications. 

The researcher has extracted a bipartite graph of authors and the papers they wrote. The dataset is located at `/home/user/wrote.csv` and has the following format:
```csv
author_id,paper_id
```
There are no headers in the actual file, just the data rows. Both `author_id` and `paper_id` are alphanumeric strings up to 32 characters long.

The researcher wants to perform a graph projection and materialization equivalent to the following Cypher query:
```cypher
MATCH (a1:Author)-[:WROTE]->(p:Paper)<-[:WROTE]-(a2:Author)
WHERE a1.id < a2.id
RETURN a1.id, a2.id, count(p) as weight
ORDER BY a1.id ASC, a2.id ASC
```

Because the dataset is quite large and this projection needs to be run repeatedly in a pipeline, the researcher wants a fast, standalone tool written in C.

Your task is to:
1. Write a C program at `/home/user/project_graph.c`.
2. The program must compile successfully using `gcc -O3 /home/user/project_graph.c -o /home/user/project_graph`.
3. The program should accept two command-line arguments: the input CSV path and the output CSV path. Example: `/home/user/project_graph /home/user/wrote.csv /home/user/coauthors.csv`.
4. The program must read the input file, materialize the co-authorship graph by counting the number of shared papers between any two authors, and export the result to the output CSV.
5. The output format must be `author1,author2,weight`, where `author1` is lexicographically less than `author2` (using standard ASCII string comparison).
6. The output rows must be sorted lexicographically by `author1` ascending, and then by `author2` ascending.
7. Run your program to process `/home/user/wrote.csv` and generate `/home/user/coauthors.csv`.

Ensure your C program is robust and efficient enough to handle tens of thousands of edges.
You are an AI assistant helping a bioinformatics researcher process and query a dataset of research papers.

The researcher has two dataset files in `/home/user/data/`:
1. `nodes.csv`: Contains paper metadata. Format: `id,year,topic`. (e.g., `105,2018,Genetics`)
2. `edges.csv`: Contains the citation graph (directed edges). Format: `source,target`. This means paper `source` cites paper `target`.

The researcher needs to perform a complex query that involves filtering, a graph join, and a centrality calculation:
"Find the in-degree (number of incoming citations) for all papers where the topic is 'Genetics' and the year is 2015 or later. Output the results sorted by in-degree in descending order, and then by id in ascending order to break ties."

Your task:
1. Write a C program at `/home/user/query.c` that efficiently performs this query. The program should be optimized (avoiding nested loops over the edges if possible, acting as an efficient query execution plan). Paper IDs are guaranteed to be integers between 1 and 100,000.
2. Compile it to `/home/user/query`.
3. The program must read `/home/user/data/nodes.csv` and `/home/user/data/edges.csv`.
4. The program must write the output to `/home/user/results.csv`.
5. The output format must be `id,in_degree` with no header row. Only include nodes that match the filter criteria. If a matching node has 0 citations, it should still be included with an in_degree of 0.

Ensure your C code compiles cleanly with standard GCC and handles file I/O appropriately. Once compiled, execute your program to generate `results.csv`.
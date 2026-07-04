You are an AI assistant helping a researcher process and analyze a dataset of academic citations. The researcher has extracted a graph of citations into a flat CSV file but needs help running complex analytical queries on it, specifically calculating recursive depths and window-like aggregations without relying on an external SQL/Graph database.

Your task is to write a C program that processes the citation dataset and extracts two specific insights. 

The dataset is located at `/home/user/citations.csv`. 
It has no header. Each line is in the format:
`citing_paper_id,cited_paper_id,year`
Where:
- `citing_paper_id` is the integer ID of the paper making the citation.
- `cited_paper_id` is the integer ID of the paper being cited.
- `year` is the integer year the citing paper was published.

Write a C program at `/home/user/process_citations.c` and compile it to an executable named `/home/user/process_citations`. The program must read `/home/user/citations.csv` and generate a report file at `/home/user/results.txt`.

The report must calculate:
1. **Longest Citation Chain:** The maximum number of edges in any directed path through the citation graph (e.g., A cites B cites C = 2 edges). You can assume the graph is a Directed Acyclic Graph (DAG) and fits in memory (max 1000 edges, max paper ID is 999).
2. **Top Cited Paper per Year:** For each year present in the dataset, calculate which `cited_paper_id` received the most citations *in that specific year*. If there is a tie, select the paper with the lowest `cited_paper_id`. (This simulates an analytical window function partition by year).

The output file `/home/user/results.txt` must exactly match this format:
```
Longest Chain Length: <integer>
Top Paper <year1>: <paper_id> (<count> citations)
Top Paper <year2>: <paper_id> (<count> citations)
...
```
*Note: Sort the yearly top papers in ascending order by year.*

Ensure your C code handles file reading properly and compiles with `gcc -O2 process_citations.c -o process_citations`. Run your executable to produce the final `results.txt` file.
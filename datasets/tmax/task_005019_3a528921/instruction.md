A researcher is analyzing a dataset of academic papers to understand citation networks over time. They have provided you with a graph schema represented in two CSV files:
1. `/home/user/nodes.csv`: Contains paper metadata. Format: `id,year` (e.g., `paper1,2020`)
2. `/home/user/edges.csv`: Contains citation relationships. Format: `source_id,target_id` (meaning source_id cites target_id)

Your task is to write a C program that performs graph projection, relationship mapping, and paginated sorting. 

Write your program in `/home/user/analyze_graph.c` and compile it to `/home/user/analyze` using `gcc`.

The compiled program must accept three command-line arguments:
`./analyze <min_year> <page_size> <page_number>`

The program should:
1. Read the nodes and edges from the CSV files.
2. Materialize a subgraph by filtering the graph to ONLY include nodes (papers) where `year >= min_year`.
3. Filter the edges to only include relationships where BOTH the `source_id` and `target_id` exist in the materialized subgraph.
4. Calculate the in-degree (number of incoming citations) for each node in this new subgraph.
5. Sort the resulting nodes by their in-degree in descending order. If there is a tie, sort them alphabetically by `id` in ascending order.
6. Apply pagination based on the provided `<page_size>` and `<page_number>` (where page_number is 1-indexed. Page 1 starts at index 0, Page 2 starts at index `page_size`, etc.).
7. Print the paginated results to standard output, one per line, in the format `id,in_degree`.

Constraints:
- You may assume `id` strings are at most 50 characters.
- You can assume there are at most 10,000 nodes and 50,000 edges.
- Use standard C libraries only.

Example: If the materialized, sorted graph has 10 nodes, and you run `./analyze 2018 3 2`, the program should print the 4th, 5th, and 6th nodes in the sorted list.
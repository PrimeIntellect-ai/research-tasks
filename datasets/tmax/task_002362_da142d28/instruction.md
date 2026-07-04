I am a researcher organizing a large dataset of academic papers, and I need to extract specific citation metrics. The dataset spans three different formats:
1. **Relational Data**: `/home/user/dataset/papers.csv` (Format: `id,title,year`)
2. **Graph Data**: `/home/user/dataset/citations.txt` (Format: `source_id target_id` representing a citation from source to target)
3. **Document Data**: `/home/user/dataset/metadata.json` (Format: An array of JSON objects, each with `"id"` and a `"keywords"` array).

I need you to write a C program that performs a cross-representation query and calculates subgraph metrics. Specifically, the program must:
1. Filter the dataset to only include papers published in or after `2015`.
2. Compute the "filtered in-degree" for each paper in this subset (i.e., the number of citations it received *only* from other papers published in or after 2015).
3. Sort the papers by this filtered in-degree in descending order. Resolve ties by sorting by `id` in ascending order.
4. Extract the top 20 papers (pagination constraint).
5. For these top 20 papers, retrieve their keywords from `metadata.json`.
6. Write the results to `/home/user/top_papers.out` in exactly this format per line:
   `ID:<id> | CITATIONS:<count> | KEYWORDS:<kw1>,<kw2>,...`

To parse the JSON, I have vendored the `cJSON` library source code (version 1.7.15) at `/app/cJSON-1.7.15`. However, I tried to compile it earlier and the Makefile seems to be broken due to an environment/configuration typo I made. You will need to fix the `Makefile` or build configuration for `cJSON`, compile it, and link it to your program.

Your C code should be saved at `/home/user/analyze.c` and compiled to `/home/user/analyze`. 

**Performance Requirement**: The dataset is quite large (~100,000 nodes and 500,000 edges). A naive nested-loop join will be too slow. You must optimize your query plan (e.g., using hash maps, binary search, or proper indexing arrays in C) so that the execution time of `/home/user/analyze` is strictly less than 0.5 seconds. 

Please fix the vendored package, write the optimized C program, compile it, and generate `/home/user/top_papers.out`.
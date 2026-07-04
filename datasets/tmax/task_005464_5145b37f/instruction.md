You are helping a bioinformatics researcher analyze a large biological knowledge graph. The researcher wants to compute the shortest unweighted path lengths between thousands of protein pairs. 

They have provided you with a custom, high-performance C tool called `kg-path-finder`, located at `/app/kg-path-finder-0.9`. Unfortunately, the tool currently produces incorrect path lengths for subsequent queries after the first one, and it runs much slower than expected.

Here are your instructions:
1. Navigate to `/app/kg-path-finder-0.9`. 
2. Identify and fix the logical bug in the graph traversal logic (likely in `src/bfs.c`) that causes subsequent path queries to return incorrect distances.
3. Optimize the `Makefile` so that the compiled binary is highly performant (e.g., adding standard compiler optimization flags).
4. Recompile the tool.
5. Run the tool using the dataset and query files located in the home directory:
   - Graph dataset: `/home/user/bio_network.tsv` (Format: `SourceNode\tTargetNode`)
   - Queries: `/home/user/protein_queries.tsv` (Format: `SourceNode\tTargetNode`)
6. Save the standard output of the tool to `/home/user/query_results.csv`. The tool outputs results in the format `SourceNode,TargetNode,Distance`. If no path exists, the distance should be output as `-1`.

An automated grading script will evaluate your `/home/user/query_results.csv` against a golden reference. Your solution must achieve a Mean Absolute Error (MAE) of exactly 0.0 on the distances, and your execution of the binary must complete in under 0.5 seconds.
You are assisting a researcher who is organizing a large catalog of datasets. To understand the relationships between different datasets, the researcher models them as a knowledge graph where datasets are connected if they share one or more categorical "tags".

The researcher wrote a C program, located at `/home/user/dataset_graph/analyzer.c`, to calculate the "degree centrality" of each dataset. In this context, the degree centrality of a dataset is defined as the **number of unique other datasets** it shares at least one tag with. 

However, the program is outputting incorrect, inflated centrality scores. The researcher suspects there is a logical flaw akin to an "implicit cross join" in SQL: the program currently counts another dataset multiple times if they share multiple tags, and it also incorrectly includes the dataset itself in its own count.

Your task:
1. Navigate to `/home/user/dataset_graph/`.
2. Inspect and fix the logic in `analyzer.c` so that it correctly calculates the degree centrality (unique shared neighbors, excluding self).
3. The program must sort the results by centrality score in descending order. If two datasets have the same score, sort them by Dataset ID in ascending order (alphabetically or numerically as strings, e.g., 'D1' comes before 'D2').
4. Implement pagination/filtering in the C code to output only the top 5 datasets.
5. Compile the program (`gcc analyzer.c -o analyzer`) and run it.
6. Make the program write the final top 5 results to `/home/user/dataset_graph/top_datasets.txt` in the exact format: `DatasetID:Score` (one per line).

Note: The graph data is already provided in `/home/user/dataset_graph/graph_data.csv`. Do not modify the CSV file.
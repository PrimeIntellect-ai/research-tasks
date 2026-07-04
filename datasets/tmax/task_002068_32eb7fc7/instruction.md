You are a performance engineer analyzing a scientific computing pipeline. We have a C program located at `/home/user/app/mesh_align.c` that performs several tasks:
1. Reshapes observational spatial data by reading `/home/user/app/observations.csv` (Format: `NodeID,X,Y,DNA_Sequence`).
2. Builds a spatial mesh graph by calculating distances between nodes.
3. Aligns a specific target primer sequence against all node sequences to find the best match candidates.

Currently, the program is unacceptably slow due to a performance bottleneck in how it processes the sequences and graph nodes.

Your task:
1. Review and compile `/home/user/app/mesh_align.c`. You may want to profile it (e.g., using `gprof` or `perf`) to identify the bottleneck.
2. Modify the C code to optimize the bottleneck. The logic must remain mathematically equivalent (the scoring rules and sorting order must be preserved), but it should run efficiently (under 1 second).
3. Compile your optimized version into an executable named `/home/user/app/mesh_align_opt`.
4. Run your optimized executable. It should generate a file `/home/user/app/top_nodes.txt` containing the `NodeID` and `Score` of the top 5 highest-scoring nodes, sorted in descending order of their score.

The output format in `/home/user/app/top_nodes.txt` must be exactly 5 lines, for example:
```
NodeID: 402, Score: 850
NodeID: 15, Score: 820
...
```

Do not change the scoring logic or the file paths. Only fix the performance issues (e.g., algorithmic inefficiencies, redundant calculations).
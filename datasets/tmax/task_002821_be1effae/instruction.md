You are a Database Reliability Engineer (DBRE) responsible for the integrity of our graph database backups. Our backup system exports nightly snapshots as plain-text directed edge lists. To quickly validate that the backup graph's structural topology hasn't been corrupted during export, we run a suite of sample shortest-path queries on the dumped edge list and aggregate the results.

We use a custom C utility linked against the `igraph` library for this validation. Unfortunately, our infrastructure currently has a broken vendored version of `igraph`, and our validation tool needs to be rewritten to match our strict new oracle specifications.

Your task has two parts:

Part 1: Fix and Build the Vendored `igraph` Library
1. The source code for `igraph` version 0.10.4 is vendored at `/app/igraph-0.10.4`. 
2. A recent errant script injected a deliberate syntax error (an `#error` directive) into the shortest path implementation (`src/paths/unweighted.c`). 
3. Find and remove this perturbation.
4. Build and install the `igraph` library. You can install it locally (e.g., to `/home/user/local`) or globally if permissions allow, but ensure your custom tool can link against it.

Part 2: Write the Backup Validator in C
1. Write a C program at `/home/user/graph_validator.c` that builds a directed graph from an edge list and answers shortest path queries.
2. The program must read from `stdin` and write to `stdout`.
3. Input Format:
   - Line 1: `V E` (number of vertices, number of edges). Vertices are 0-indexed (0 to V-1).
   - The next `E` lines contain two integers each: `u v`, representing a directed edge from `u` to `v`.
   - The next line contains `Q` (number of validation queries).
   - The next `Q` lines contain two integers each: `start end`.
4. Output Format:
   - For each of the `Q` queries, print the shortest path distance (number of edges) from `start` to `end` on a single line.
   - If the `end` vertex is unreachable from the `start` vertex, print `-1`.
5. Compile your program to an executable at `/home/user/graph_validator`, dynamically linking against your fixed `igraph` library.

Your program's output will be strictly tested against a reference oracle to ensure absolute correctness on thousands of randomly generated backup topologies. Ensure your program handles disconnected components and cycles correctly.
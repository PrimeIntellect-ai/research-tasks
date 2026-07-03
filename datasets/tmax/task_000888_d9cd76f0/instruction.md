You are a performance engineer analyzing the execution traces of a large-scale scientific numerical simulation. Some configurations of the simulation cause catastrophic performance degradation due to near-infinite recursive loops in the numerical solvers. We need to automatically filter out these "divergent" configurations before they are submitted to our HPC cluster.

Your task is to create a C++ classifier that identifies whether a given application call graph configuration will perform well ("CLEAN") or diverge ("EVIL").

1. **Extract Specifications**: You have been provided with an image at `/app/profile_specs.png`. Use OCR (e.g., `tesseract`) to extract the exact `TIMEOUT_THRESHOLD` and `MONTE_CARLO_RUNS` values from this image.
2. **Understand the Graph Format**: We have two directories of sample call graphs: `/app/corpora/clean/` and `/app/corpora/evil/`. 
   Each file represents a probabilistic call graph. 
   - The first line contains `N`, the number of functions (nodes 0 to N-1). Node 0 is the `ENTRY` function. Node N-1 is the `EXIT` function.
   - The next `N` lines contain the base execution cost (a floating-point number) for each function.
   - The remaining lines define directed edges in the format: `SourceNode DestinationNode TransitionProbability`. The probabilities for all outgoing edges from a given node sum to 1.0. The `EXIT` node has no outgoing edges.
3. **Build the Simulator / Classifier**: Write a C++ program that takes a path to a graph file as its first command-line argument.
   - The program must simulate the execution path using a **Monte Carlo simulation**.
   - For `MONTE_CARLO_RUNS` iterations, simulate a random walk starting at Node 0 and ending at Node N-1. 
   - Accumulate the execution cost for each visited node (including repeated visits).
   - If the *average* total execution cost across all Monte Carlo runs strictly exceeds `TIMEOUT_THRESHOLD`, the configuration is considered divergent.
   - The program must print exactly `EVIL` to standard output (with a newline) if it diverges, or `CLEAN` if it is well-behaved.
4. **Output Requirements**: 
   - Compile your C++ source code to `/home/user/profile_analyzer`.
   - Your executable must handle exactly one argument (the file path): `/home/user/profile_analyzer <path_to_graph_file>`
   - Do not output any extra text to `stdout` other than `CLEAN` or `EVIL`. You may use `stderr` for debugging.

Develop and test your C++ program using the provided corpora. Your final compiled executable will be tested against a hidden set of clean and evil graphs.
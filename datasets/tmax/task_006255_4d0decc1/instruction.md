You are a data engineer working on an ETL pipeline migration. We are migrating our pipeline dependency graph into a NoSQL graph database, but first, we need a tool to analyze the current hierarchical dependencies and extract specific execution patterns.

I have placed a tab-separated file representing our knowledge graph of pipeline tasks at `/home/user/pipeline_deps.tsv`. Each line represents a directed dependency between two tasks in the format:
`Source_Task    Target_Task`

Your objective is to write a C++ program that reads this file, reconstructs the graph, and performs a recursive hierarchical query to find all valid end-to-end execution chains. A valid chain is defined as any path that starts with the task exactly named `Extract_Root` and ends with the task exactly named `Load_Final`.

Instructions:
1. Write a C++ program at `/home/user/find_chains.cpp`.
2. The program should read from `/home/user/pipeline_deps.tsv`.
3. It should recursively traverse the graph to find all paths from `Extract_Root` to `Load_Final`.
4. The output must be written to a file at `/home/user/chains.txt`.
5. In `/home/user/chains.txt`, print each discovered path on a new line. The tasks in the path must be separated by ` -> ` (space, dash, greater-than, space). 
6. The paths in the output file must be sorted alphabetically to ensure consistent verification.
7. Compile your C++ program using `g++ -O2 -std=c++17 /home/user/find_chains.cpp -o /home/user/find_chains` and run it to produce the output.

Ensure your C++ code correctly handles directed acyclic graph (DAG) traversals and properly formats the output.
You are acting as a database administrator. A junior team member attempted to export an execution dependency graph of our nightly batch jobs into a CSV file located at `/home/user/query_plan.csv`. 

Unfortunately, their SQL export query contained an implicit cross join. As a result, the CSV contains many spurious edges connecting unrelated jobs. The file format is supposed to be:
`ParentJob,ChildJob,ExecutionCost`

You know that valid dependency edges always have an `ExecutionCost` strictly less than 1000. Any edge with a cost of 1000 or greater is a spurious result from the implicit cross join and must be ignored. 

Your task is to write a C++ program at `/home/user/process_graph.cpp` that:
1. Reads `/home/user/query_plan.csv`.
2. Validates the schema (ignores any malformed lines that do not strictly match the `String,String,Integer` format).
3. Filters out the implicit cross join edges (cost >= 1000).
4. Computes the shortest execution path (minimum total cost) from the node `START` to the node `END` using the valid edges.
5. Writes ONLY the optimal path to `/home/user/optimized_path.txt` in the exact format: `Node1->Node2->...->NodeN`.

Compile your code using `g++` and run it to produce the output file.
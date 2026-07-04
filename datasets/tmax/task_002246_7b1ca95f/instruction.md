You are assisting a database researcher in organizing and analyzing complex dataset transaction graphs. The researcher is studying concurrent transaction deadlocks by looking at dependency graphs where nodes are transactions and edges are locks with specific wait-time weights.

The researcher has an old proprietary tool, located at `/app/deadlock_oracle`, which processes these transaction graphs to find the "critical lock path capacity." Unfortunately, the source code for this tool was lost, and it is a stripped binary. The researcher needs you to create an equivalent open-source implementation in C++ that can be integrated into their modern NoSQL aggregation pipelines.

Your task:
1. Analyze the `/app/deadlock_oracle` binary to understand its input/output behavior. 
   - The binary reads from Standard Input (stdin).
   - The first line of input contains four integers: `N M S T`, representing the number of transactions (nodes), the number of dependencies (edges), the starting transaction ID, and the target transaction ID. Nodes are 0-indexed.
   - The next `M` lines contain three integers each: `u v w`, representing a directed dependency from transaction `u` to transaction `v` with a lock weight of `w`.
   - The binary outputs a single integer to Standard Output (stdout).

2. Write a C++ program at `/home/user/deadlock_solver.cpp` that perfectly replicates the behavior of `/app/deadlock_oracle`. 
   - Your program must use the exact same input/output format.
   - Compile your program to `/home/user/solver` using `g++ -O3 /home/user/deadlock_solver.cpp -o /home/user/solver`.

The final executable `/home/user/solver` will be tested against the original `/app/deadlock_oracle` using hundreds of randomly generated transaction dependency graphs. Your implementation must produce bit-exact equivalent output for all inputs. If no path exists, make sure to observe and replicate how the oracle handles it.
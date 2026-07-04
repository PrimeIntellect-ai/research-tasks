We are migrating our build dependency resolver into a minimal "scratch" Docker container. Our current tool is a dynamically-linked executable that is both bloated and extremely slow on large dependency graphs.

We have provided the legacy binary at `/app/legacy_resolver` (which you can use as a black-box reference) and a sample dependency graph at `/app/deps.txt`.

Your task is to write a highly optimized, statically compiled C replacement.

### Requirements:
1. **Algorithm**: The program must read a text file containing directed edges and calculate the length (number of edges) of the **longest path** in the dependency graph.
2. **Cycle Detection**: Some of our build graphs accidentally contain circular dependencies. If the graph contains a cycle, the program must print exactly `CYCLE` to stdout and exit with status code `1`.
3. **Output**: If it is a valid Directed Acyclic Graph (DAG), print the integer length of the longest path to stdout and exit with status code `0`.
4. **Static Binary**: You must compile your C code to `/home/user/fast_resolver` as a fully static executable so it can run in a scratch container. Include necessary optimization flags, as your program will be rigorously benchmarked.

### Input Format (`deps.txt`):
Each line contains two strings separated by a space, representing a directed edge from the first node to the second. Node names are alphanumeric and up to 31 characters long. 
Example:
```
moduleA moduleB
moduleA moduleC
moduleC moduleD
```
*(In this example, the longest path is moduleA -> moduleC -> moduleD, which has a length of 2 edges).*

### Verification:
An automated test suite will verify your binary (`/home/user/fast_resolver`) against a hidden, massive evaluation graph. Your tool must output the exact same integer as `/app/legacy_resolver` but achieve a **runtime speedup of at least 10x**. You are encouraged to use a linear-time $O(V+E)$ algorithm (e.g., memoization/Dynamic Programming) since the legacy tool uses a naive approach.
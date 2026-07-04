You are a Database Reliability Engineer. We manage a complex, distributed database cluster where backups are taken as a graph of dependent jobs. 

We have a proprietary compiled utility, `/app/backup_route_calc`, that parses our backup dependency graphs and calculates critical metrics for backup scheduling. Unfortunately, the source code was lost, and we need to replace it with a verifiable, optimized C++ implementation.

Your task is to reverse-engineer the behavior of `/app/backup_route_calc` and write a functionally identical C++ program.

**Input/Output Specifications:**
The binary reads from standard input and writes to standard output.
The input format represents a directed graph of backup jobs and a series of queries:
1. Two integers `N` and `M` (number of jobs, number of dependencies). Nodes are 0-indexed (`0` to `N-1`).
2. `M` lines, each containing three integers `u`, `v`, and `w` (indicating job `u` must transfer data to job `v` with a bandwidth cost of `w`).
3. An integer `Q` (number of queries).
4. `Q` lines representing queries. Each query starts with an integer `T` (the query type), followed by arguments.

**Query Types to Reverse Engineer:**
- **Type 0:** Takes one argument `u`. (You need to deduce what metric it calculates for job `u` by testing the binary).
- **Type 1:** Takes two arguments `u` and `v`. (You need to deduce what it calculates between job `u` and `v`. Hint: It relates to optimal routing cost. If a condition isn't met, it outputs `-1`).

**Requirements:**
1. Experiment with `/app/backup_route_calc` to understand exactly what Type 0 and Type 1 queries compute.
2. Write a C++ source file at `/home/user/route_calc.cpp` that perfectly mimics this behavior.
3. Compile it to `/home/user/route_calc` (e.g., `g++ -O3 -std=c++17 /home/user/route_calc.cpp -o /home/user/route_calc`).
4. Your program must handle multiple queries efficiently (consider query plan interpretation and optimal data structures). 

The automated test will rigorously fuzz your compiled executable against the original stripped binary with random graphs and queries to ensure bit-exact equivalence.
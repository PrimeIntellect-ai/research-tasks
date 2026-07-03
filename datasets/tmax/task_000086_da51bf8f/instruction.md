You are a data analyst working with a custom knowledge graph exported as CSV files. Your goal is to materialize this graph in memory using C, optimize the querying process, and extract a specific sub-graph pattern.

You have two input files:
1. `/home/user/nodes.csv`
   Format: `node_id,node_type` (both integers)
   Node types: `1` (Person), `2` (City)

2. `/home/user/edges.csv`
   Format: `source_id,target_id,relation_type` (all integers)
   Relation types: `1` ("knows", directed from Person to Person), `2` ("lives_in", directed from Person to City)

Write and execute a C program (e.g., `/home/user/query.c`) that reads these CSV files and finds all instances of the following pattern:
- Person `A` "knows" Person `B` (Relation type 1: A -> B)
- Person `A` "lives_in" City `C` (Relation type 2: A -> C)
- Person `B` "lives_in" City `C` (Relation type 2: B -> C)

Your C program should be optimized. An unoptimized O(E^3) scan will be too slow for large datasets, so you should build an efficient in-memory projection (like an adjacency list or hash index) to match this pattern quickly.

Your program must output the matching patterns to `/home/user/matches.csv`.
The output file must contain comma-separated values in the format `A_id,B_id,C_id` with one match per line.
Sort the output lines ascending by `A_id`, then `B_id`, then `C_id`.

Constraints & Details:
- Only use standard C libraries (e.g., `stdio.h`, `stdlib.h`, `string.h`).
- Compile your program using `gcc`.
- `node_id` values fit within standard 32-bit signed integers.
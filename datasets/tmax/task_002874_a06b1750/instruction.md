You are acting as a technical assistant to a compliance officer. We are auditing a complex system of cascading service permissions (a knowledge graph of access controls) to ensure there are no unauthorized backdoor access paths.

To do this, we are using an internal C library, `libkggraph` (version 1.2.0). The source code for this library is vendored at `/app/libkggraph-1.2.0`.

However, the library currently has a problem: our compliance queries are failing to detect transitive access paths that are more than 1 hop deep. I suspect there is a deliberate or accidental misconfiguration in the library's build system (Makefile or headers) limiting the traversal depth. 

Your tasks:
1. Investigate `/app/libkggraph-1.2.0`. Find and fix the perturbation that restricts graph traversal depth (we need it to support at least a depth of 1024). Recompile the library.
2. Write a C program at `/home/user/audit_checker.c` and compile it to `/home/user/checker`. Your program must link against the fixed `libkggraph`.
3. `/home/user/checker` must read from standard input (`stdin`) and write to standard output (`stdout`).

**Input Format (stdin):**
- Line 1: Two integers `N` (number of nodes, 0 to `N-1`) and `E` (number of edges).
- Next `E` lines: Three integers `U V R` representing an edge from `U` to `V` with role level `R` (1 to 5). This means `U` delegates permissions to `V`.
- Next line: One integer `Q` (number of audit queries).
- Next `Q` lines: Two integers `X Y`.

**Query Logic:**
For each query `X Y`, output `1` if there is a directed path from `X` to `Y` where *every* edge on that path has a role level `R >= 3`. Otherwise, output `0`. Use the library's `kg_check_transitive(graph, start, end, min_role)` function to compute this.

**Output Format (stdout):**
- Exactly `Q` lines containing `1` or `0`.

The `libkggraph.h` header provides:
```c
typedef struct kg_graph_t kg_graph_t;
kg_graph_t* kg_create(int num_nodes);
void kg_add_edge(kg_graph_t* g, int u, int v, int role);
int kg_check_transitive(kg_graph_t* g, int start_node, int end_node, int min_role);
void kg_destroy(kg_graph_t* g);
```

Please fix the library, write the integration code, and ensure `/home/user/checker` is fully functional and perfectly accurate.
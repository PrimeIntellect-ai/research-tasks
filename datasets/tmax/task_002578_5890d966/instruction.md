You are acting as an AI assistant to a compliance officer who is auditing our internal infrastructure for data leakage risks. 

We need to ensure there are no unauthorized pathways from our sensitive databases to public-facing endpoints. We have a graph representing network access flows between various services, databases, and external endpoints. 

Your task is to create a C++ tool and a bash pipeline to analyze this schema, map the relationships, and compute the shortest violation paths.

Here is what you need to do:

1. **Write a C++ program** named `/home/user/audit_paths.cpp`.
   - The program must take exactly one command-line argument: the absolute path to a classification file (`/home/user/node_classifications.txt`).
   - The program must read network edges from standard input (`stdin`). Each line of stdin will contain an active edge in the format `SourceNode,TargetNode` (representing a directed access flow from SourceNode to TargetNode).
   - The program must parse the classifications. The classification file contains lines in the format `NodeName:Classification`, where Classification is either `Sensitive`, `Internal`, or `Public`.
   - The program must build a directed graph and compute the shortest path (fewest edges) from *any* `Sensitive` node to *any* `Public` node.
   - If a path exists, it must output the absolute shortest path found across all Sensitive/Public pairs. If there is a tie for the shortest path length, resolve the tie by selecting the path that is lexicographically first when comparing the full path string (e.g., `A -> B -> C` comes before `A -> Z -> C`).
   - The output must be printed to standard output in exactly this format:
     `VIOLATION: Node1 -> Node2 -> Node3`
   - If no such path exists, output exactly: `COMPLIANT: No paths found`
   - Compile this program to `/home/user/audit_paths` using `g++ -std=c++17`.

2. **Create a bash pipeline script** named `/home/user/audit_pipeline.sh`.
   - The script must parse our raw access logs located at `/home/user/raw_schema_edges.csv`.
   - The raw file has three columns: `Source,Target,Status`.
   - Use standard bash utilities (like `grep`, `awk`, `cut`, etc.) to filter this file so that ONLY rows with the status `Active` are kept, and extract only the `Source,Target` columns.
   - Pipe this filtered output directly into your compiled `/home/user/audit_paths` executable, passing `/home/user/node_classifications.txt` as the argument.
   - Redirect the final output of the C++ program to `/home/user/audit_report.txt`.

Ensure `/home/user/audit_pipeline.sh` is executable. You should run the script to generate `/home/user/audit_report.txt` as your final step.
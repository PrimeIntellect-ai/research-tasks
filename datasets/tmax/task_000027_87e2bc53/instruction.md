As a researcher organizing large citation datasets, you need to query a directed citation network efficiently without a formal database. You must implement a custom index strategy and graph traversal using pure Bash and coreutils.

The dataset is located at `/home/user/network.tsv`. It is a tab-separated file with two columns: `Source` and `Target`, representing directed edges in the network.

Your task is to write two Bash scripts:

1. **Index Generation (`/home/user/setup_index.sh`)**:
   This script must read `/home/user/network.tsv` and create a directory named `/home/user/graph_index/`. To allow fast O(1) lookups in Bash, for every unique `Source` node, it should create a text file named `<Source>.txt` in this directory. The file must contain all `Target` nodes that the `Source` node points to, with one node per line, sorted alphabetically.

2. **Graph Traversal (`/home/user/query_traversal.sh`)**:
   This script will take a single argument: the starting node ID (e.g., `./query_traversal.sh NodeA`).
   It must use the files in `/home/user/graph_index/` to find all nodes that are at exactly a distance of 2 from the starting node in the directed graph (i.e., reachable via exactly two edges: Start -> Intermediate -> Destination).
   
   **Constraints for the traversal:**
   - The destination node cannot be the starting node itself.
   - The destination node cannot be a direct neighbor (distance 1) of the starting node.
   - You must count the number of unique paths (Intermediate nodes) that lead to each valid distance-2 destination node.
   
   The script must output the top 5 destination nodes with the highest path counts to `stdout`. The output must be sorted by count descending, and then by node name ascending in case of a tie.
   
   **Output Format:**
   `Node,Count`
   (e.g., `NodeZ,4`)

Ensure both scripts have execute permissions (`chmod +x`). 
You can test your implementation by creating a small `network.tsv` manually before relying on the main dataset.
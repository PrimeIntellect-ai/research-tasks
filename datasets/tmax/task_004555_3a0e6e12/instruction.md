You are a performance engineer profiling a new distributed graph analytics application on a Linux cluster. Before running the full MPI profile, you need to set up the environment and perform a baseline graph topology analysis using Bash.

You have been provided with an HDF5 file located at `/home/user/network.h5`. This file contains the edge list of a molecular graph under two datasets:
- `/links/source` (integer node IDs)
- `/links/target` (integer node IDs)

Your task consists of two parts:

1. **Parallel Computing Setup**: 
   The application requires an MPI hostfile. Create a file named `/home/user/hostfile` that defines 4 worker nodes named `worker-0`, `worker-1`, `worker-2`, and `worker-3`. Configure each node to have exactly 8 slots.

2. **Graph Analysis via Bash**:
   Write an executable Bash script at `/home/user/analyze.sh`. This script must:
   - Read the source and target node IDs from `/home/user/network.h5`. You may use `h5dump` or write a minimal inline Python/h5py command within the Bash script to dump the arrays.
   - Treat the graph as undirected (a node's degree is the total number of times it appears in either the source or target datasets).
   - Calculate the degree of every node using standard Bash utilities (e.g., `awk`, `sort`, `uniq`).
   - Identify the node with the highest degree.
   - Output the result to `/home/user/max_degree.txt` exactly in this format: `Node ID: X, Degree: Y` (where X is the node ID and Y is its degree). If there is a tie, output the one with the lowest Node ID.

Make sure your script is executable and run it so that `/home/user/max_degree.txt` is generated before you finish the task.
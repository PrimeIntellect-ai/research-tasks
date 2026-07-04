As a machine learning engineer, you are preparing node-level training features for a Graph Neural Network (GNN). You have been given a C++ feature extraction program `/home/user/extract.cpp` that calculates the "mean neighbor degree" for each node in a molecular or interaction graph.

However, the current C++ implementation fails regression tests because it exhibits numerical instability. Specifically, it generates `NaN` (Not a Number) values for disconnected/isolated nodes due to a division by zero.

Your task is to:
1. Fix the numerical instability in `/home/user/extract.cpp`. If a node has a degree of 0, its mean neighbor degree should be explicitly set to `0` to prevent division by zero.
2. Compile the fixed C++ code to an executable at `/home/user/extract`.
3. Run the executable on the provided graph edge-list `/home/user/graph.txt`. Save the raw output (which prints `NodeID MeanNeighborDegree` on each line) to `/home/user/features.txt`.
4. Create a bash script at `/home/user/density.sh` that reads `/home/user/features.txt` and performs basic density estimation by binning the mean neighbor degree values (the second column) into the following bins:
   - Bin 0: value is exactly 0
   - Bin 1: 0 < value <= 1
   - Bin 2: 1 < value <= 2
   - Bin 3: value > 2
5. Execute `/home/user/density.sh` so that it calculates the bin counts and writes them to `/home/user/density.log` in exactly this format:
```
Bin 0: <count>
Bin 1: <count>
Bin 2: <count>
Bin 3: <count>
```

Ensure that your bash script functions correctly and relies only on standard Linux coreutils/shell built-ins (e.g., `awk`, `grep`, `bash`).
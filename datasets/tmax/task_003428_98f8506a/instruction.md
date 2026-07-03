You are a data scientist analyzing the topological properties of a molecular network. You have been provided with the network's topology and need to evaluate how well the distribution of shortest path lengths matches a proposed analytical model.

Your task is to write a C program that computes the all-pairs shortest paths for the graph, derives the empirical probability distribution of these distances, compares it to the theoretical distribution using the Total Variation Distance (TVD), and outputs the results.

**Input Data:**
- A file located at `/home/user/molecule.edgelist` contains the edges of the undirected, unweighted graph.
- Each line contains two space-separated integers `u` and `v` representing an edge between node `u` and node `v`. The nodes are 0-indexed and contiguous up to $N-1$ (you can determine $N$ by finding the maximum node ID in the file + 1). The graph is guaranteed to be fully connected.

**Algorithm & Mathematical Requirements:**
1. **Empirical Distribution:**
   - Compute the shortest path distance $d$ between all unique pairs of distinct nodes $(u, v)$ where $u < v$.
   - Find the maximum shortest path distance in the graph, which is the network's diameter ($D$).
   - Calculate the empirical probability distribution $P_{emp}(d)$ for $d \in \{1, 2, ..., D\}$. 
   - $P_{emp}(d) = \frac{\text{number of pairs with distance } d}{N(N-1)/2}$.

2. **Theoretical Distribution:**
   - The proposed analytical model for the path lengths follows a truncated Poisson-like shape.
   - For $d \in \{1, 2, ..., D\}$, the unnormalized theoretical weight is given by $T(d) = \frac{3^d}{d!}$.
   - Calculate the normalized theoretical probability distribution $P_{theory}(d) = \frac{T(d)}{\sum_{k=1}^D T(k)}$.

3. **Total Variation Distance (TVD):**
   - Calculate the Total Variation Distance between the empirical and theoretical distributions:
   - $TVD = \frac{1}{2} \sum_{d=1}^D \left| P_{emp}(d) - P_{theory}(d) \right|$

**Execution & Output:**
1. Write your C code in `/home/user/model_fit.c`.
2. Compile and run your program. You may use standard C libraries (e.g., `stdio.h`, `stdlib.h`, `math.h`, etc.). Ensure you link the math library if necessary (e.g., `-lm`).
3. Your program must create a log file exactly at `/home/user/fit_results.txt` with the following format:
```
Diameter: [D]
TVD: [TVD rounded to exactly 4 decimal places]
```
For example:
```
Diameter: 5
TVD: 0.1234
```

Do not output anything else to this text file.
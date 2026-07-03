A bioinformatics pipeline for analyzing sequence transition graphs is failing. We model sequence transitions as a directed graph and attempt to find the stationary distribution of the Markov chain by solving a linear system. However, the transition matrix is near-singular because some sequence states act as sinks (e.g., absorbing states), causing our standard matrix solver to fail.

I have an image located at `/app/network_params.png` that contains the edge list for a specific sequence motif graph and a regularization parameter, `Alpha`. 

Please write a C++ program named `/home/user/resolve_network.cpp` that does the following:
1. Constructs the adjacency matrix from the edges found in the image.
2. Converts it into a transition probability matrix (rows sum to 1; if a row has no outgoing edges, it transitions to itself).
3. Applies a teleportation/regularization factor using the `Alpha` value extracted from the image. Specifically, with probability `1 - Alpha`, follow the graph transition, and with probability `Alpha`, jump to any node uniformly at random. This fixes the near-singular matrix issue.
4. Solves the resulting linear equations to find the stationary distribution $\pi$.
5. Calculates the Kullback-Leibler (KL) divergence between the computed stationary distribution $\pi$ and a uniform distribution $U$ (where $U_i = 1/N$ for $N$ nodes). Use the natural logarithm.
6. Prints ONLY the final KL divergence as a floating-point number to standard output.

You may use standard C++ libraries. Do not use external linear algebra libraries; you can implement a simple iterative power method or Gaussian elimination to solve the system, as the graph is small (under 10 nodes). Use `tesseract` to read the image. Compile the code using `g++` and run it. Provide the output.
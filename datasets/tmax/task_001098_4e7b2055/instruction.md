You are a DevOps engineer assisting with forensic log analysis. We use a custom C++ tool called `fast-log-cluster` to group similar log events, but the tool is currently broken and cannot process our latest batch of logs. 

The source code for the tool is located at `/app/fast-log-cluster`. It processes vectorized log representations and uses a k-means clustering approach.

Currently, the tool suffers from two main issues:
1. **Dependency Conflict**: The build system is pointing to an outdated, bundled math library (`vendor/math_v1`) which contains buggy distance calculation routines. The package includes a fixed `vendor/math_v2`, but the `Makefile` and includes are misconfigured.
2. **Convergence Failure**: Even when built, the clustering algorithm hangs indefinitely on the dataset `/app/forensic_logs.txt`. The algorithm fails to converge. You will need to trace the intermediate state of the cluster centroids to diagnose the oscillation and implement a proper convergence fix in the C++ code.

Your objectives:
1. Resolve the dependency conflict so the project builds using `math_v2`.
2. Debug and fix the convergence issue in `src/cluster.cpp`. Ensure that the clustering loop terminates correctly when the centroids stabilize.
3. Compile the fixed tool.
4. Run the tool on the provided dataset to generate 5 clusters:
   `./fast_log_cluster /app/forensic_logs.txt 5 > /home/user/centroids.txt`

The file `/home/user/centroids.txt` must contain exactly 5 lines, each representing the final coordinates of a cluster centroid as a comma-separated list of floating-point numbers.

An automated verifier will evaluate the mathematical accuracy of your centroids against the known ground truth. You must achieve a Mean Squared Error (MSE) of less than 0.01.
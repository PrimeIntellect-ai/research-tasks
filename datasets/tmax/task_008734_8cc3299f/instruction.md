You are a performance engineer working on a structural biology pipeline. The current legacy application reads Protein Data Bank (PDB) files, computes the structural principal components, and evaluates a density integral along the principal axis. However, you've discovered a critical issue: because the legacy tool uses multi-threading with an indeterminate floating-point reduction order, the covariance matrix and subsequent Singular Value Decomposition (SVD) yield slightly non-reproducible results across different runs.

Your task is to write a robust, deterministic replacement tool from scratch in your language of choice. You must guarantee exact bitwise reproducibility by enforcing a strict reduction order, regardless of how the data was read. 

Here are your precise specifications:

1. **Input Parsing**: 
   - Read the file `/home/user/input.pdb`.
   - Parse all lines starting exactly with `ATOM  `. 
   - Extract the X, Y, and Z coordinates. In standard PDB format, these are at columns 31-38, 39-46, and 47-54 respectively.

2. **Canonical Ordering**:
   - To guarantee reproducible summation order, you must sort the extracted (X, Y, Z) coordinate tuples lexicographically in ascending order (sort by X; if tied, sort by Y; if tied, sort by Z) *before* performing any summations.

3. **Centroid & Covariance (Matrix Decomposition)**:
   - Compute the centroid (mean of X, Y, Z) by summing the coordinates in the strictly sorted order.
   - Subtract the centroid from each point to get centered coordinates.
   - Compute the 3x3 covariance matrix $C = P^T P$, where $P$ is the $N \times 3$ matrix of centered coordinates. Again, build this matrix by summing the outer products of the centered points in the canonical sorted order.
   - Perform a Singular Value Decomposition (SVD) on $C$ such that $C = U \Sigma V^T$.

4. **Numerical Integration**:
   - Identify the dominant principal axis (the left singular vector in $U$ corresponding to the *largest* singular value). Ensure the direction of this vector has a positive X component; if its X component is negative, multiply the vector by -1 (if X is exactly 0, check Y, etc., to make it deterministic).
   - Evaluate the line integral of a pseudo-electron density $\rho(p)$ along this principal axis vector $\vec{v}$, parameterized by $p(t) = \text{centroid} + t \cdot \vec{v}$.
   - The density function is: $\rho(p) = \sum_{i=1}^N \exp(-0.1 \cdot ||p - P_i||^2)$, where $P_i$ are the original uncentered atomic coordinates.
   - Integrate $\rho(p(t))$ from $t = -10.0$ to $t = 10.0$ with respect to $t$.
   - Use the Trapezoidal rule with exactly $N_{steps} = 1000$ equal-width intervals (i.e., 1001 evaluation points).

5. **Outputs**:
   Save your results in the following files, formatting all floating-point numbers to exactly 6 decimal places:
   - `/home/user/centroid.txt`: A single line with the X, Y, and Z coordinates of the centroid, comma-separated (e.g., `1.234567,2.345678,3.456789`).
   - `/home/user/singular_values.txt`: A single line with the three singular values of $C$ in descending order, comma-separated.
   - `/home/user/integral.txt`: A single line with the numerical value of the integral.

You may use any programming language (Python, C++, Rust, etc.) and any standard math libraries available or installable via the system package manager or language-specific package manager (e.g., `pip`, `apt`).
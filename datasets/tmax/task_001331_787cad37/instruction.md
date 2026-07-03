**Final Objectives & Specifications:**
1. **TCP Service:** Implement a C++ TCP server listening on `127.0.0.1:9090`.
2. **Oracle Interrogation:** A stripped binary exists at `/app/jacobian_oracle`. It simulates the local Jacobian matrix of our fluid dynamics model at a given coordinate. You must reverse-engineer its CLI invocation and output format to extract the 3x3 matrix.
3. **Protocol Details:** The server must accept raw newline-terminated TCP string queries and respond with newline-terminated strings:
   - `EIGEN <x> <y>\n`: Execute a convergence test (power iteration) on the 3x3 matrix at coordinate `(x, y)` to find the dominant eigenvalue. Respond with the single float value.
   - `QR_R <x> <y>\n`: Perform QR decomposition on the matrix at `(x, y)`. Respond with the 3 diagonal elements of the upper triangular matrix $R$, space-separated.
4. **Data Visualization:** Produce a file `/home/user/eigen_vis.csv` containing the dominant eigenvalues for a 2D grid. The grid must cover $x \in [0.0, 1.0]$ and $y \in [0.0, 1.0]$ in increments of $0.1$. The CSV header must be `x,y,eigenvalue`.

You must implement the matrix math and the TCP server entirely in C++. Standard POSIX/Linux APIs are permitted. The server should remain running in the background.
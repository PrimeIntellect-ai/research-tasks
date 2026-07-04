You are a performance engineer tasked with optimizing a bioinformatics simulation bottleneck. Our research pipeline currently relies on a slow, proprietary simulation binary to compute the structural stability of DNA sequences using a Monte Carlo approach. 

We need you to build a high-performance, drop-in replacement service in C++.

**The Legacy Oracle:**
There is a stripped, legacy binary located at `/app/legacy_oracle`. You can execute it from the command line to observe its input/output format, but it is far too slow for production.
Usage: `/app/legacy_oracle <fasta_sequence> <cov_00> <cov_01> <cov_10> <cov_11>`
Output: A single floating-point number representing the stability score.

**The Algorithm:**
Through previous analysis, we know the binary performs the following:
1. Takes a DNA sequence string (only to compute its length $N$) and a 2x2 symmetric positive-definite covariance matrix $\Sigma$.
2. Performs a Cholesky decomposition of $\Sigma = L L^T$.
3. Uses a Monte Carlo simulation with $M = 100,000$ iterations. 
4. For each iteration, it generates $N$ correlated 2D steps. To do this, it initializes a standard C++ Mersenne Twister (`std::mt19937`) seeded with the value $N$. 
5. For each step $k$ from $1$ to $N$, it generates two independent standard normal random variables (using `std::normal_distribution<double>(0.0, 1.0)`). It multiplies this 2D vector by $L$ to get a correlated 2D step $(x_k, y_k)$.
6. The score for a single iteration is the maximum $x$ value achieved during the $N$ steps minus the minimum $y$ value achieved during the $N$ steps.
7. The final stability score is the average of these iteration scores over the $M$ iterations.

**Your Goal:**
Write a C++ application (save it as `/home/user/sim_server.cpp`) that exposes this optimized calculation as a TCP server.
1. The server must listen on `127.0.0.1:9000`.
2. It should accept incoming TCP connections.
3. The client will send a single line of text formatted exactly as: `<fasta_sequence>,<cov_00>,<cov_01>,<cov_10>,<cov_11>\n`
4. The server must parse this, compute the stability score using the exact algorithm described above, send the result back as a string formatted to 4 decimal places (e.g., `4.5678\n`), and close the connection.
5. Compile your server to `/home/user/sim_server` using `g++ -O3 -pthread`.
6. Start the server in the background so it is ready to receive requests.

Ensure your pseudo-random number generation sequence exactly matches the standard C++ implementation to achieve equivalence with the legacy oracle.
You are a performance engineer responsible for maintaining our scientific computing pipeline. We rely on a vendored C++ matrix decomposition library called `libsvd_fast` located in `/app/libsvd_fast` to perform SVDs. 

Recently, our daily regression tests started failing. Profiling indicates two major issues with the SVD component:
1. The execution time has severely regressed.
2. The probability distribution of the computed singular values diverges significantly from our theoretical baseline, causing downstream statistical analysis to fail. The reconstruction error matrix norm is unacceptably high.

Your task is to:
1. Identify and fix the two bugs introduced in `/app/libsvd_fast`. One is a build configuration issue crippling performance, and the other is an algorithmic parameter in the SVD source code destroying precision.
2. Build and install the fixed `libsvd_fast` library. Install the headers and compiled shared library into `/home/user/local/`.
3. We have provided a regression test program at `/home/user/regression_test.cpp`. Compile this program against your fixed library. The program generates a random test matrix, computes the SVD, and measures both the execution time and the Frobenius norm of the reconstruction error ($||A - U \Sigma V^T||_F$).
4. Run the compiled regression test. It will output a file named `/home/user/metrics.json` containing the profiling results.

Ensure your fixes result in a mathematically correct SVD decomposition that runs efficiently. 

Leave the compiled test executable at `/home/user/run_test` and the output metrics at `/home/user/metrics.json`.
You are acting as a performance engineer working on a spectral analysis pipeline. We have a proprietary, stripped legacy binary located at `/app/spectra_oracle` that simulates the spectral response of a chemical sample given three spatial parameters: `x`, `y`, and `z`. 

Your task is to build a C++-based optimization service that finds the optimal `x, y, z` parameters to reproduce a given target spectrum.

Here is what you need to do:
1. Reverse-engineer or treat `/app/spectra_oracle` as a black box. It takes three floating-point arguments (`x`, `y`, `z`) in the range `[0.0, 10.0]` and prints a 10-point spectrum as comma-separated values to standard output.
2. Write a C++ application that implements an optimization routine (e.g., Nelder-Mead simplex, gradient descent, or adaptive grid refinement) to find the `x, y, z` parameters that minimize the Mean Squared Error (MSE) between the oracle's output and a target spectrum.
3. Your C++ application must run an HTTP server listening on TCP port `8080` on `127.0.0.1`.
4. The server must accept a `POST` request at the endpoint `/optimize`. The body of the request will be a plain text string of 10 comma-separated floats (the target spectrum).
5. The server must run the optimization using the `/app/spectra_oracle` binary and respond with an `HTTP/1.1 200 OK` containing a plain text body of the optimal `x, y, z` values, comma-separated. The values must be accurate to within +/- 0.1 of the true optimal values.
6. The service must handle multiple sequential requests.

Ensure your code compiles with `g++ -O3`. Start the server in the background once compiled.
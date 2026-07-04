You are an AI assistant acting as a performance engineer. We have a performance bottleneck in a mathematical pipeline that involves estimating the integral of a highly peaked function, which behaves similarly to a matrix factorization failing on near-singular inputs due to the sharp gradients. 

Your task is to implement a parallelized Monte Carlo estimator for this integral as a microservice.

Step 1: Extract Configuration
There is an image file located at `/app/config.png`. This image contains a single text line specifying a critical parameter for the function, formatted as `COEFF=<value>`. Extract this value using OCR (e.g., `tesseract`).

Step 2: Implement the Monte Carlo Estimator in C
Write a C program (save it as `/home/user/mc_integral.c`) that estimates the definite integral of the function:
f(x) = 1 / (x^2 + COEFF)
over the interval [0, 1] using a Monte Carlo integration method (uniformly sample x in [0, 1] and compute the average of f(x)).

Requirements for the C program:
- It must use OpenMP to parallelize the random sampling.
- Ensure proper thread-safe random number generation to avoid false convergence or race conditions (e.g., using `rand_r` with different seeds per thread).
- It should accept two command-line arguments: `<num_samples>` and `<num_threads>`.
- The program should set the number of OpenMP threads to `<num_threads>`.
- It should print ONLY the final estimated integral as a floating-point number to stdout.

Compile the C program to `/home/user/mc_integral` with OpenMP enabled.

Step 3: Serve via HTTP
Set up a simple HTTP server (you may use Python's `http.server`, `Flask`, or any lightweight web framework) listening exactly on `127.0.0.1:8080`.
The server must expose a single GET endpoint: `/simulate`.
It should accept two query parameters: `samples` (integer) and `threads` (integer).
When this endpoint is hit, the server must execute your compiled C program with the provided arguments, capture the output, and return an `application/json` response with the format:
`{"result": <estimated_value>}`

Ensure the server is left running in the background so it can be queried by our automated test suite.
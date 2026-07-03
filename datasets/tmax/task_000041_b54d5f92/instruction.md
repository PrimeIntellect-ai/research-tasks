You are an acoustics researcher developing a specialized simulation microservice in Go. The system models the steady-state response of a simple 3-element acoustic metamaterial when subjected to an excitation force derived from a real audio recording. 

Your objective is to implement the solver, write a regression test for the numerical methods, and expose the results via an HTTP API.

Step 1: Audio Analysis
There is a 16-bit PCM mono WAV file located at `/app/source.wav`. 
Write Go code to parse this WAV file (you must write a basic parser using `encoding/binary` and `os`, without relying on third-party audio libraries). 
Find the maximum absolute amplitude (peak 16-bit integer value) across the entire audio data chunk. Let this float64 value be `M`.

Step 2: Numerical Matrix Solver
The acoustic medium is modeled as a 3-element discretized system represented by the tridiagonal stiffness matrix A:
A = [[4, -1, 0], 
     [-1, 4, -1], 
     [0, -1, 4]]

The excitation force vector `b` is derived from the audio peak amplitude `M`:
b = [M, M/2.0, M/4.0]

To solve the system `A * x = b` for the displacement vector `x`, you must implement an LU decomposition algorithm from scratch in Go. Do not use external libraries like Gonum. Your code should decompose A into lower and upper triangular matrices, and then use forward and backward substitution to find `x`.

Step 3: Regression Testing
In `/home/user/sim_server/math_test.go`, write a standard Go test suite (`go test`) that tests your LU decomposition and substitution solver against a known baseline:
Test matrix `A_test = [[2, 1], [1, 2]]` and `b_test = [3, 3]`. The test should assert that the solution is `[1, 1]` (within a small float tolerance).

Step 4: Multi-protocol Web Service
Create an HTTP server in `/home/user/sim_server/main.go`.
The server must listen on `127.0.0.1:9090`.
It should expose a single endpoint: `GET /solve`
When a request is received, it should return a JSON response with the following exact structure:
```json
{
  "max_amplitude": 12345.0,
  "solution": [x0, x1, x2]
}
```
(Replace 12345.0 with the actual value of `M`, and x0, x1, x2 with the computed float64 solutions).

Run the server in the background so it is actively listening on port 9090 when you finish. Do not shut it down.
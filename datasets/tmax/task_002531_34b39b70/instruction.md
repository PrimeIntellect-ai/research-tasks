You are a Machine Learning Engineer preparing a synthetic dataset of 2D thermal distributions to train a surrogate neural network. The physical system is a 2D metal plate with a highly localized heat source. 

Your task is to build a hybrid pipeline that extracts design parameters from a schematic, simulates the thermal distribution in C++, and serves the data generator via an HTTP API for the ML training loop to consume.

Step 1: Parameter Extraction (Image Fixture)
There is a schematic image of the new plate design located at `/app/heat_schematic.png`. Use an OCR tool (like `tesseract`, which is installed) to read the text from this image. You are looking for the exact coordinates of the primary heat source, formatted like "SOURCE_COORD: X=<val>, Y=<val>". You will need these coordinates (integers) for your simulation.

Step 2: Thermal Simulation Engine (C++)
Write a C++ program (which can be called by or wrapped in a web server) that models the steady-state heat equation (Poisson's equation $\nabla^2 T = -Q$) on a 50x50 grid.
- **Multi-dimensional array manipulation & Mesh refinement**: Represent the plate as a 50x50 grid. The boundaries of the plate ($x=0, x=49, y=0, y=49$) are held constantly at $T=0$.
- **Convergence testing**: Solve the PDE using the iterative Jacobi or Gauss-Seidel method. Stop the iteration when the maximum temperature change across the grid between consecutive iterations is less than `1e-4`. 
- **MCMC Sampling**: The simulation must take a `target_peak` temperature. Implement a simple Metropolis-Hastings MCMC sampler to find the unknown heat source intensity $Q$ that results in the simulation having a maximum grid temperature within $\pm 0.5$ degrees of `target_peak`. Assume a Gaussian proposal distribution for $Q$. The heat source $Q$ is applied exactly at the $(X, Y)$ coordinate extracted from the image. 
- **Curve fitting**: Once a valid $Q$ is found and the grid is solved, extract the 1D horizontal slice of temperatures along the row $y=Y$ (the same Y as the source). Perform a quadratic least-squares polynomial fit ($T(x) = ax^2 + bx + c$) on this 1D profile.

Step 3: Data Generator Service (Multi-protocol)
The ML training loop expects to fetch data dynamically via HTTP.
Create a server (you may use a simple Python HTTP server that invokes your C++ binary, or write it natively in C++) that listens on `127.0.0.1:8080`.
- **Endpoint**: `GET /generate?target=<float>`
- **Behavior**: The server must run the C++ simulation pipeline targeting the requested peak temperature, find the corresponding $Q$, solve the grid, fit the curve, and return an HTTP 200 response with a JSON payload.
- **Response Format**: `{"Q": <float>, "a": <float>, "b": <float>, "c": <float>}`

Constraints:
- You must write the core simulation, MCMC, and curve fitting logic from scratch in C++. Standard library only for the math.
- The HTTP server must remain running in the background listening on port 8080 so the automated test suite can verify it.
You are a performance engineer profiling and migrating a slow scientific pipeline. We currently analyze particle trajectories from experimental videos, fit a nonlinear model via MCMC (Markov Chain Monte Carlo), and serve predictions over a network. The current implementation is too slow, and you need to build a high-performance replacement in C.

Here are your instructions:

1. **Video Analysis**:
   - You are provided a video artifact at `/app/trajectory.mp4`.
   - The video is exactly 20 frames long (1 fps), with a resolution of 1000x1000 pixels.
   - The background is pure black (RGB: 0, 0, 0).
   - In each frame, there is exactly one pure white pixel (RGB: 255, 255, 255) representing the particle.
   - Extract the (X, Y) coordinates of the particle in each frame, where X is the column index (0-999) and Y is the row index (0-999). Keep them in frame order (frame 0 to 19). 

2. **MCMC Parameter Estimation**:
   - The particle's motion is governed by the nonlinear equation: `Y = A * X^2 + B * X + C`
   - Write a C program that takes the extracted (X, Y) dataset and implements a Metropolis-Hastings MCMC sampler to estimate the parameters A, B, and C.
   - Your MCMC implementation must run for at least 100,000 iterations to ensure convergence, discarding the first 10% of samples as burn-in. Compute the mean of the posterior distribution for A, B, and C.

3. **Multi-Protocol Service**:
   - You must expose your prediction model as an HTTP service listening exactly on `127.0.0.1:8080`.
   - You may write the HTTP server natively in C or use tools like `socat` to wrap your C executable.
   - The service must accept HTTP GET requests to the endpoint `/predict?x=<value>`, where `<value>` is an integer.
   - The service MUST enforce authentication. It should only process requests that include the HTTP header: `Authorization: Bearer perf-token-2024`. Reject requests without this header.
   - The service must respond with an `HTTP/1.1 200 OK` status and a plain text body containing ONLY the predicted `Y` value as an integer (round the floating-point result to the nearest integer) using your estimated posterior mean parameters.

Write your code, compile it (GCC is available), test it, and leave the HTTP service running in the background. Do not exit the terminal until the service is up and listening.
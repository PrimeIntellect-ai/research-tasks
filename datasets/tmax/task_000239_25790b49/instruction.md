You are a bioinformatics analyst working on a new sequence processing pipeline. We have a microservice architecture that provides configuration parameters for our sequence smoothing algorithm. 

Currently, our microservices are broken. There is a Redis instance and a Flask API. The Flask API is supposed to provide parameters for our PDE (Partial Differential Equation) based sequence smoothing model, but it is currently crashing because it cannot connect to Redis.

Your tasks are:
1. **Fix the Services**: The services are located in `/app/`. Redis is running on the default port (6379). The Flask app (`/app/api.py`) reads the Redis port from the `REDIS_PORT` environment variable (defaulting to 6380 if not set). Create a wrapper script or modify the environment to start the Flask app on port 5000 so that it successfully connects to Redis. 
2. **Write the Sequence Processor**: Create a standalone Python script at `/home/user/process_seq.py` that takes a single DNA sequence string as a command-line argument.
   - The script must first make a GET request to `http://localhost:5000/api/params` to retrieve a JSON object containing the diffusion constant `alpha` and iterations `N`.
   - Convert the input DNA sequence into a 1D numpy array of floats where 'C' and 'G' are 1.0, and 'A' and 'T' are 0.0.
   - Smooth this binary signal using the 1D heat equation (explicit finite difference method) for `N` iterations. 
     - The update rule is: $u_i^{(n+1)} = u_i^{(n)} + \alpha (u_{i+1}^{(n)} - 2u_i^{(n)} + u_{i-1}^{(n)})$.
     - Use Dirichlet boundary conditions fixed at 0.0 for both ends (i.e., $u_0 = 0$ and $u_{L-1} = 0$ for all time steps, where $L$ is the length of the sequence).
   - After `N` iterations, calculate the mean of the smoothed array.
   - Print a comma-separated list of the 0-based indices where the smoothed value is strictly greater than the mean.

The automated verification system will fuzz your `/home/user/process_seq.py` script with thousands of random DNA sequences and compare its output against a compiled oracle. Ensure your mathematical operations strictly follow the update rule and your output formatting is exact.
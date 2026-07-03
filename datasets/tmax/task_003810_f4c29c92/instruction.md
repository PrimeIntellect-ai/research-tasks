You are a data scientist studying the diffusion of a fluorescently tagged protein in a microfluidic channel.

We have a video recording of the experiment and the structure of the protein tracer. You need to analyze the video, calculate the theoretical and experimental diffusion properties, and serve the results via an HTTP API for our automated lab system to query.

Here are the specific requirements:

1. **Protein Parsing (Bioinformatics)**:
   - Read the PDB file located at `/app/tracer.pdb`.
   - Count the total number of Alpha Carbon atoms (atom name `CA`). Let this be $N$.
   - Calculate a reference constant $k = N / 100.0$.

2. **Video Analysis & Reshaping**:
   - A video of the diffusion process is located at `/app/diffusion.mp4`.
   - The video is 10 seconds long at 30 fps. Extract frames corresponding to exactly $t = 0, 1, 2, \dots, 9$ seconds (e.g., frames 0, 30, 60, etc.).
   - Convert each extracted frame to grayscale.
   - For each frame, compute the 1D concentration profile by summing the pixel intensities along each column (resulting in a 1D array of length equal to the video width).

3. **Mathematical Fitting (Linear/Nonlinear Solving)**:
   - For each 1-second interval $t$, fit a Gaussian function to the 1D profile to find its spatial variance $\sigma^2(t)$ (in squared pixels).
   - Use linear regression on the relationship $\sigma^2(t) = 2 D_{app} t + C$ to solve for the apparent diffusion coefficient $D_{app}$ (in pixels^2 / second).

4. **API Service (Multi-Protocol)**:
   - Create a Python-based HTTP web service (you may use Flask, FastAPI, or standard library `http.server`) listening exactly on `127.0.0.1:8000`.
   - All endpoints must require an `Authorization` header with the exact value `Bearer diff_token_99`. If missing or incorrect, return a `401 Unauthorized` status code.
   - Implement a `GET /stats` endpoint that returns a JSON response in the following format:
     `{"N": <integer>, "k": <float>, "D_app": <float>}`
   - (Round `D_app` to 2 decimal places in the JSON).
   - Leave the server running in the background. Write your server process ID to `/home/user/server.pid` so we know it has started.

Work in `/home/user/workspace`. Do not stop until the web service is fully operational and the PID file is created.
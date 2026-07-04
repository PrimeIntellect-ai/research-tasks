You are a bioinformatics analyst studying the motility of a novel microorganism. We have a fluorescence microscopy video of a single organism moving over time. Your task is to extract its trajectory, model its movement using C, compare two competing hypotheses statistically, and serve the results via an HTTP API.

Part 1: Video Extraction
You are provided a video at `/app/fluorescence.mp4`. It contains 100 frames (at 10 fps) showing a single bright white dot (the organism) on a solid black background.
Extract the (X, Y) pixel coordinates of the centroid of the dot for each frame (from frame 0 to 99). 

Part 2: Kinematic Modeling in C
Write a C program (`/home/user/model.c`) that:
1. Reads the extracted sequence of (X,Y) coordinates.
2. Represents the trajectory as a 2D multi-dimensional array.
3. Fits the X-coordinates to a linear equation: $X(t) = V_x \cdot t + X_0$.
4. Fits the Y-coordinates to a nonlinear equation: $Y(t) = Y_0 + V_y \cdot t + A \cdot \sin(\omega \cdot t)$. Use a simple iterative nonlinear solver (e.g., Newton-Gauss or random search) to estimate $A$ and $\omega$ (assume $\omega$ is between 0.05 and 0.2 rad/frame).
5. Performs a statistical hypothesis comparison: Calculate the Sum of Squared Errors (SSE) for the Y-coordinates using a simple linear model ($A=0$) versus the nonlinear model ($A \neq 0$). Output the F-statistic for the comparison.

Part 3: API Service
Create a service that listens on `127.0.0.1:8080` (you may use a simple Python HTTP server that calls your compiled C binary, or write it directly in C).
The server must implement the following GET endpoints:
- `/api/trajectory` : Returns a JSON array of objects `[{"frame": 0, "x": 100.0, "y": 100.0}, ...]`.
- `/api/parameters` : Returns a JSON object with the solved parameters from the C program: `{"vx": float, "x0": float, "y0": float, "vy": float, "A": float, "omega": float}`.
- `/api/stats` : Returns a JSON object `{"f_statistic": float, "better_model": "linear" | "nonlinear"}`. (Select "nonlinear" if F > 3.0).

Requirements:
- The API must be running and available for testing on `127.0.0.1:8080`.
- Write your C code in `/home/user/model.c` and compile it to `/home/user/model`.
- Start your server in the background so the test script can query it.
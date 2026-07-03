You are a data scientist analyzing continuous spatial-spectroscopy data. We have a sensor service that provides spectral readings at specified spatial coordinates, but our initial model fitting pipeline fails because the numerical integration of the signal diverges (inaccurately overestimates the area) due to a uniform, coarse step size missing sharp signal peaks.

Your task is to write a script to interact with this service, apply signal denoising, perform adaptive mesh refinement, and evaluate the final signal distribution against a baseline.

Here are the specific requirements:

1. **Start the Sensor Service:**
   There is a python script located at `/home/user/sensor_service.py` that provides a REST API. Start it in the background. It listens on `http://127.0.0.1:8000`.
   - Endpoint: `GET /data?x=<float>`
   - Returns a JSON array of 5 spectral frequency readings for the coordinate $x$.

2. **Develop the Analysis Script:**
   Write a script in any language you prefer (Python is highly recommended) that does the following:
   
   **Phase A: Initial Sampling & Denoising (SVD)**
   - Query the sensor service for an initial uniform spatial mesh $x \in [0, 1]$ with a step size of $0.1$ (i.e., $x = 0.0, 0.1, 0.2, \dots, 1.0$).
   - Construct a matrix $M$ of size $N \times 5$ where $N$ is the number of spatial points.
   - Perform Singular Value Decomposition (SVD) on $M$. Reconstruct the matrix $M_{denoised}$ using **only the top 2 singular values** (set the rest to zero).
   - Compute the summary signal $S(x) = \sum_{j=1}^{5} M_{denoised}(x, j)^2$ for each point.

   **Phase B: Adaptive Mesh Refinement**
   - The initial mesh is too coarse and misses a sharp structural peak. Implement an adaptive domain decomposition:
   - Iterate over your sorted spatial points. For any adjacent pair $(x_i, x_{i+1})$, if $|S(x_i) - S(x_{i+1})| > 0.5$, compute the midpoint $x_{mid} = (x_i + x_{i+1}) / 2$.
   - Query the API for $x_{mid}$, insert it into your mesh, compute its denoised signal using the *same* SVD projection (do not recompute the SVD of the whole matrix, just project the new 5-vector onto the top 2 principal components obtained in Phase A, and compute its $S(x_{mid})$).
   - Repeat this refinement until no adjacent points have a signal difference $> 0.5$.

   **Phase C: Distribution Distance Metric**
   - Numerically integrate $S(x)$ over your refined, non-uniform mesh $x$ using the trapezoidal rule to find the total area $A$.
   - Normalize the signal to create a probability density function: $P(x) = S(x) / A$.
   - Using your final refined spatial points $x$ as observations, compute the 1-D Wasserstein distance between the empirical distribution defined by $P(x)$ over $x$, and a standard uniform distribution $U(0,1)$. (If using Python, `scipy.stats.wasserstein_distance` using $x$ as values and $P(x)$ as weights against a uniform sample is acceptable, or calculate the integral of the absolute difference of their CDFs).
   - *Precision constraint:* Compare the CDF $C(x) = \int_0^x P(t) dt$ (using cumulative trapezoidal rule) with the uniform CDF $C_{unif}(x) = x$. Calculate the discrete $L_1$ Wasserstein distance exactly as: $\sum_{i=1}^{N-1} \frac{x_{i+1} - x_i}{2} \left( |C(x_i) - x_i| + |C(x_{i+1}) - x_{i+1}| \right)$.

3. **Output:**
   Save ONLY the final calculated distance (as a floating-point number, rounded to 6 decimal places) to `/home/user/result.txt`.
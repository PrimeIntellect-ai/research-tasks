You are a data scientist tasked with fitting a linear dynamic system model to physical movement captured in a video. 

We have recorded a video of a particle's movement at `/app/movement.mp4`. The video contains a single white particle moving against a black background.

Your task involves several stages:
1. **Video Processing**: Extract the frames from `/app/movement.mp4`.
2. **Trajectory Extraction**: Write a Go program that processes these extracted frames **in parallel** (using Go concurrency) to compute the centroid (x, y coordinates) of the white particle in each frame.
3. **Model Fitting**: We assume the particle follows a linear discrete-time dynamic system: $X_{t+1} = A X_t$, where $X_t = \begin{bmatrix} x_t \\ y_t \end{bmatrix}$ and $A$ is a $2 \times 2$ transition matrix. 
   Write a Go script to estimate the matrix $A$ using least squares fitting. To ensure **numerical stability**, you MUST use **QR decomposition** (e.g., via the `gonum.org/v1/gonum/mat` package) to solve the overdetermined system, rather than computing the normal equations ($X^T X$) directly.
4. **Service Integration**: Expose your fitted model as an HTTP service. Your Go program must start an HTTP server listening on exactly `127.0.0.1:8080`.
   
The HTTP server must support the following endpoints:
* `GET /matrix`: Returns the estimated transition matrix $A$ as a JSON response in the format:
  `{"a11": float, "a12": float, "a21": float, "a22": float}`
* `GET /predict?t=<frame_index>`: Takes an integer `t` and returns the predicted position of the particle at frame `t` (starting from the initial position $X_0$ at `t=0`, computed as $A^t X_0$). Response format:
  `{"x": float, "y": float}`

Constraints:
- You must use Go as the primary programming language for the extraction, fitting, and server logic.
- Ensure your Go module is properly initialized and dependencies (like Gonum) are fetched.
- Leave the HTTP server running in the foreground or background so that it can be tested.
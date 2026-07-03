You are an ML engineer preparing training data for a physics-informed neural network. We have raw video footage of a projectile motion experiment in `/app/experiment.mp4`. Your goal is to extract the frames, isolate the moving object using dimensionality reduction, fit its trajectory to a curve, and optimize a physical parameter model to estimate the local gravity $g$.

Please complete the following workflow:

1. **Environment Setup & Orchestration:**
   Create a bash script at `/home/user/run_pipeline.sh` that first uses `ffmpeg` to extract all frames from `/app/experiment.mp4` into a directory `/home/user/frames/` as grayscale PNGs at 30 FPS.

2. **Primary Implementation (Go):**
   Write a Go program at `/home/user/analyze.go`. You should use the `gonum.org/v1/gonum` package (you will need to initialize a Go module in `/home/user`). 
   The Go program must:
   - Read the grayscale frames.
   - Perform Matrix Decomposition (e.g., SVD) to separate the static background from the moving object (the projectile).
   - Extract the 2D coordinates (x, y) of the projectile's centroid for each frame.
   - Perform Curve Fitting (regression) on the extracted points to model the parabolic trajectory.
   - Implement an Optimization routine (gradient descent) to estimate the underlying gravity parameter $g$ based on the equation $y(t) = y_0 + v_{y0} t + \frac{1}{2} g t^2$ (assuming the scale is 100 pixels = 1 meter and $t$ is calculated from the 30 FPS frame rate). Include Convergence testing to stop the gradient descent once the change in the loss function falls below $10^{-6}$.

3. **Output:**
   The Go program must output the final estimated gravity parameter and the fitted coefficients to a JSON file at `/home/user/results.json` with the following exact structure:
   ```json
   {
     "estimated_gravity": 9.85,
     "trajectory_coefficients": [c0, c1, c2],
     "optimization_steps_taken": 142
   }
   ```

Make sure your `run_pipeline.sh` script executes the Go program after extracting the frames. You may use standard CLI tools and Go standard libraries along with Gonum.
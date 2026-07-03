You are an MLOps engineer tasked with analyzing an automated physics experiment run. The experiment was recorded, and we need to extract the trajectory of the projectile, apply a smoothing model, and track the experiment metadata.

There is a video artifact located at `/app/experiment_run.mp4`. The video features a bright white projectile moving across a dark background.

Your task is to build a C++ pipeline that does the following:
1. **Analysis Environment Setup:** Create a CMake-based C++ project in `/home/user/tracker/`. Assume `libopencv-dev` is already installed on the system.
2. **Video Processing:** Write a C++ program using OpenCV to read `/app/experiment_run.mp4`. For each frame, isolate the white projectile (e.g., via simple binary thresholding) and compute its center of mass (centroid x and y coordinates).
3. **Model Evaluation / Smoothing:** The raw centroid coordinates will have some noise. Implement a smoothing algorithm in C++ (e.g., a simple Moving Average with a window size of 5, or a Kalman filter) to smooth the `x` and `y` trajectories.
4. **Experiment Tracking:** 
   - Save the smoothed trajectory to `/home/user/smoothed_tracking.csv` with the header exactly as: `frame,x,y`. Frame indices must start at 0.
   - Save an experiment tracking log to `/home/user/experiment_log.json` with the following format:
     ```json
     {
       "run_name": "physics_01",
       "model": "moving_average",
       "num_frames": <total_frames_processed>
     }
     ```

Build and run your pipeline. The output `smoothed_tracking.csv` will be evaluated against a hidden ground-truth trajectory using a Mean Squared Error (MSE) metric to verify the accuracy of your tracking and smoothing model.
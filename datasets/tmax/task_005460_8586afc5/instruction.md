You are assisting a computational physics researcher. We have been running Monte Carlo simulations of particle diffusion, but we suspect a floating-point reduction order bug on our new cluster is causing non-reproducible results. This bug manifests as sudden, anomalous shifts in the probability distribution of particle energies between consecutive simulation steps.

We have a reference video of a visually stable simulation, and two corpora of raw simulation traces. 

Your task is to build a robust detection pipeline:

1. **Reference Video Calibration**:
   - Extract the frames from the reference video located at `/app/reference_simulation.mp4` using `ffmpeg`.
   - Convert the frames to grayscale.
   - For each frame, compute a 256-bin grayscale histogram (bins 0-255).
   - Calculate the 1D Wasserstein distance (`scipy.stats.wasserstein_distance`) between the histograms of consecutive frames.
   - Find the maximum consecutive Wasserstein distance in this reference video. Let's call this `D_ref`.

2. **Simulation Trace Analysis & Optimization**:
   - We have simulation trace data in two directories: `/app/corpus/clean/` (stable, reproducible runs) and `/app/corpus/evil/` (runs affected by the reduction order bug).
   - Each trace is a CSV file where each row represents a simulation timestep, containing 256 comma-separated integers representing the energy histogram at that step.
   - You need to write an optimization routine to find an optimal threshold distance `T` (which will be a scalar multiple of `D_ref`) that perfectly separates the clean traces from the evil traces based on their maximum consecutive-timestep Wasserstein distance.

3. **Detector Implementation**:
   - Create a final Python script at `/home/user/detector.py` that takes a single command-line argument: the path to a simulation trace CSV file.
   - The script must compute the maximum consecutive-step Wasserstein distance for the provided CSV.
   - If this maximum distance is strictly greater than your optimized threshold `T`, the script must print exactly `REJECT` to standard output.
   - If the distance is less than or equal to `T`, it must print exactly `ACCEPT`.

Your solution must correctly classify 100% of the clean corpus as ACCEPT and 100% of the evil corpus as REJECT. 
Ensure your script uses standard libraries, `numpy`, and `scipy`. You can test your pipeline iteratively against the provided `/app/corpus` directories.
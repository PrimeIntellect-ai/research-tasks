You are an MLOps engineer responsible for recovering and tracking lost experiment artifacts from a recent physical simulation run. The metadata pipeline crashed during the experiment, but we still have the raw sensor feed video. 

Your task is divided into two parts: Video Data ETL and Statistical Tooling.

Part 1: Video Artifact ETL Pipeline
1. We have a sensor video artifact located at `/app/sensor_feed.mp4`. 
2. Set up an analysis environment by creating `/home/user/experiment_artifacts/frames/` and `/home/user/scripts/`.
3. Use `ffmpeg` (preinstalled) to extract the first 20 frames of the video at 1 frame per second (FPS), starting from the very beginning. Extract them as grayscale `pgm` (Portable Gray Map) images into the `frames` directory, naming them `frame_01.pgm`, `frame_02.pgm`, etc.
4. The video contains two distinct sensor regions. For each extracted frame, you need to calculate the average pixel intensity of the top-left 50x50 block (Sensor X) and the bottom-right 50x50 block (Sensor Y). Store these ordered values in a tabular text file at `/home/user/experiment_artifacts/sensor_data.csv` with columns `frame,sensor_x,sensor_y`.

Part 2: Bash Covariance Utility
Our automated artifact tracking service requires a standalone, ultra-portable Bash utility to compute tracking metrics on the fly. You must reconstruct the covariance calculation model using purely Bash and standard Linux tools (like `awk` or `bc`).
1. Create a script at `/home/user/scripts/calc_cov.sh`.
2. The script must accept an arbitrary even number of integer arguments (passed directly as command-line arguments: `$1`, `$2`, etc.).
3. The first half of the arguments represents an array of values for Variable A. The second half represents Variable B. (e.g., if 10 arguments are passed, args 1-5 are A, args 6-10 are B).
4. The script must compute the **sample covariance** between A and B. 
   Formula: `Cov(A, B) = Sum( (A_i - mean_A) * (B_i - mean_B) ) / (n - 1)`
   where `n` is the number of pairs.
5. Finally, multiply the resulting sample covariance by `1000`, truncate it to an integer (drop the decimal part completely, e.g., `-12.8` becomes `-12`), and print ONLY this final integer to standard output.
6. The script must be bit-exact in its mathematical outputs for any valid array of integers, as it will be rigorously tested against a reference oracle via randomized fuzzing.

Ensure `/home/user/scripts/calc_cov.sh` is executable.
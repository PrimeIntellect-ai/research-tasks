You are acting as a data science assistant for a physics researcher who is organizing datasets derived from video recordings of a fluid dynamics experiment. 

We have a raw video recording of the experiment located at `/app/experiment_run.mp4`. We also have two datasets of pre-extracted feature vectors (describing particle kinematics over time windows) derived from similar videos. One dataset contains clean, valid experimental data (`/app/data/clean/`), and the other contains artificially corrupted data where tracking errors or sensor noise (like silently dropping frames leading to NaN-like interpolations that skew velocities) have been introduced (`/app/data/evil/`).

Your task is to:
1. Extract frame-by-frame data from `/app/experiment_run.mp4` using `ffmpeg` and bash tools to determine the total number of frames and the average pixel intensity of the first 10 frames. Save these two numbers (comma-separated: `total_frames,avg_intensity`) to `/home/user/video_stats.txt`.
2. Write a C++ classification program that reads a directory of feature CSV files and predicts whether each file is "clean" or "evil".
3. The C++ program must be compiled to `/home/user/classifier`.
4. The classifier should accept exactly one command-line argument: the path to a directory containing CSV files. It must output a text file named `predictions.txt` in the current working directory. Each line in `predictions.txt` should contain the filename and the prediction (0 for clean, 1 for evil), separated by a comma. Example: `sample_001.csv,1`.

The feature CSV files in the `clean` and `evil` directories contain 100 rows and 5 columns of floating-point numbers representing normalized kinematic features. The "evil" data exhibits subtle variance shifts in the 4th and 5th columns due to the interpolation errors. Your C++ model should use basic statistical features (e.g., mean and variance of specific columns) to separate them. You can use standard C++ libraries.

You must ensure your classifier correctly identifies the clean and evil samples. The researcher will run your `/home/user/classifier` against a hidden adversarial corpus consisting of similar clean and evil datasets to evaluate its robustness.
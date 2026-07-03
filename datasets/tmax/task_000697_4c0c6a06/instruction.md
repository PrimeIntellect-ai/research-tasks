I need you to build a reproducible, mathematical data-cleaning pipeline in Go that extracts telemetry from a video and then applies a strict causal filter to avoid a "future-data leakage" problem (similar to the fit_transform leakage in ML pipelines). Finally, you will build a mathematical classifier to detect if other datasets contain this leakage.

Background:
We are analyzing the trajectory of a glowing pendulum. We have a video of the experiment at `/app/dataset/pendulum.mp4` and a noisy sensor log at `/app/dataset/sensor_time.csv`. Previous data scientists applied a global moving average and global min-max normalization across the *entire* time series before feeding it into our predictive models. This caused "data leakage" because the normalization and smoothing at time `t` incorporated information from time `t+1` and beyond, making our real-time models fail in production.

Part 1: Video Extraction & Data Joining (Go & FFmpeg)
Write a Go program at `/home/user/pipeline/extract.go` that:
1. Calls `ffmpeg` to extract the frames from `/app/dataset/pendulum.mp4`.
2. Calculates the horizontal center of mass (X-centroid) of all pixels with a grayscale value > 200 for each frame.
3. Joins these X-centroids with the timestamps in `/app/dataset/sensor_time.csv` (which has a `frame_id` and `timestamp_ms` column). 
4. Saves the raw joined data to `/home/user/pipeline/raw_trajectory.csv` (columns: `frame_id`, `timestamp_ms`, `x_centroid`).

Part 2: Causal Data Cleaning
Write a Go program at `/home/user/pipeline/clean.go` that processes `raw_trajectory.csv` and outputs `/home/user/pipeline/clean_trajectory.csv` with a new column `x_smoothed_normalized`. 
Crucially, you must compute a 5-frame moving average and min-max normalization *strictly causally*. For frame `t`, the moving average must only use frames `t-4` to `t`. The min-max normalization at frame `t` must only use the minimum and maximum values seen from frame `0` up to frame `t`. Do not look ahead!

Part 3: The Leakage Detector (Adversarial Corpus)
We need to audit historical datasets to see if they were tainted by the "future-data leakage" (non-causal smoothing).
Write a Go CLI tool at `/home/user/pipeline/detector.go` that compiles to `/home/user/bin/detector`.
- It should take a single argument: the path to a trajectory CSV file (formatted like `clean_trajectory.csv` but with columns `t` and `val`).
- It must mathematically analyze the time series `val` to determine if a non-causal smoothing filter was applied. (Hint: look at how the smoothed signal reacts to sudden impulses/spikes. A causal filter only reacts *after* the spike. A non-causal/centered filter starts rising *before* the spike).
- The binary must exit with code 0 if the dataset is clean (strictly causal).
- The binary must exit with code 1 if the dataset is "evil" (contains future-data leakage).

We have provided two test corpora:
- `/app/corpora/clean/` (contains 50 CSV files with causally cleaned trajectories)
- `/app/corpora/evil/` (contains 50 CSV files with non-causal/future-leaked trajectories)

Verify your detector against these corpora. Your final `detector` binary must correctly accept 100% of the clean corpus and reject 100% of the evil corpus.
You are a data engineer tasked with building a robust ETL and inference pipeline for a smart traffic monitoring system. The system combines noisy radar sensor data with motion data extracted from a traffic camera video. 

You must implement the primary logic using **C**. You may use shell commands and standard tools (like `ffmpeg`) for the initial data extraction, but the data joining, Bayesian inference, experiment tracking, and network serving must be written in a C program.

Here is the pipeline specification:

**Phase 1: Video Feature Extraction & Tokenization**
1. You are provided a video file at `/app/traffic_feed.mp4` (24 frames per second).
2. Using `ffmpeg`, extract the frames to standard JPEG files.
3. Tokenize the visual motion: write a script or use standard utilities to compute the file size (in bytes) of each extracted JPEG. We will use JPEG file size as a proxy for scene complexity/motion. 
4. Downsample this data to 1-second intervals by taking the maximum JPEG file size among the 24 frames for each second (i.e., second 0 corresponds to frames 1-24, second 1 to frames 25-48). 

**Phase 2: Multi-source Data Joining**
1. You are provided a CSV file at `/app/radar_sensors.csv` with columns: `timestamp_sec`, `noisy_speed_mph`, `prior_prob_speeding`.
2. Write a C program that reads the max-JPEG-size per second from Phase 1 and joins it with `/app/radar_sensors.csv` on the `timestamp_sec` (e.g., second 0, second 1, etc.).

**Phase 3: Bayesian Inference & Experiment Tracking**
1. In your C program, implement a Bayesian update to calculate the posterior probability of a speeding violation for each second.
   - **Prior:** `prior_prob_speeding` from the CSV.
   - **Likelihood $P(Motion | Speeding)$:** If max_jpeg_size > 50000 bytes, likelihood is 0.8. Otherwise, 0.3.
   - **Likelihood $P(Motion | Not Speeding)$:** If max_jpeg_size > 50000 bytes, likelihood is 0.4. Otherwise, 0.7.
2. Track your pipeline's inference parameters. Your C program must append an experiment log to `/home/user/etl_experiment.log` in the format: `[RUN] sec=<timestamp_sec> prior=<prior> posterior=<posterior>`.

**Phase 4: Multi-protocol Serving**
1. Your C program must start an HTTP server listening on `127.0.0.1:8080`.
2. The server must accept `GET /posterior?sec=<timestamp_sec>` requests.
3. The server must enforce authorization. It should only respond with `200 OK` if the request includes the HTTP header `X-Auth-Token: etl-agent-secret`. Otherwise, return `401 Unauthorized`.
4. The successful response body should be plain text containing just the floating-point posterior probability (formatted to 4 decimal places, e.g., `0.7241`) for that specific second.

Build, compile, and run your pipeline. Leave the C server running in the background so the automated verifier can query it.
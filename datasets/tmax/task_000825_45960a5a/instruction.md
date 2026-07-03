You are a data analyst investigating a series of anomalies in an industrial manufacturing machine. You have access to a video recording of a machine test and several sensor log datasets. Your goal is to build an anomaly detector in Bash to classify log files.

**Step 1: Environment Setup**
Ensure your environment has the necessary tools for video analysis and data processing (e.g., `ffmpeg`, `imagemagick`, `awk`). 

**Step 2: Video Analysis (Ground Truth Extraction)**
You are provided a reference video of the machine running: `/app/machine_feed.mp4` (10 seconds, 10 frames per second).
During the video, the machine occasionally enters an anomalous state. This is visually indicated *only* by the top-left 10x10 pixels turning pure red (`#FF0000`).
Write a process to extract the frames, analyze the top-left 10x10 region, and record the exact timestamps (in seconds, e.g., `1.2`, `4.5`) where this anomaly indicator is present. 

**Step 3: Tabular Data Transformation & Threshold Tuning**
You are given a training CSV log of the same test run: `/app/training_log.csv`. 
The CSV has columns: `timestamp,sensor_alpha,sensor_beta,sensor_gamma`.
Using the timestamps you extracted from the video, cross-reference the training log. You must perform a basic hyperparameter sweep using Bash/AWK to find which sensor (alpha, beta, or gamma) strongly correlates with the anomalies, and find the exact integer threshold `N` that perfectly separates normal operation from the anomaly states. An anomaly is defined as the sensor value being strictly greater than `N`.

**Step 4: Adversarial Classification Integration**
You must write a final classification script at `/home/user/classify.sh`.
This script must:
1. Accept exactly one argument: the path to a CSV file to evaluate.
2. Parse the CSV file using Bash/AWK.
3. Apply the rule you discovered (e.g., if `sensor_X > N` anywhere in the file).
4. Print exactly `EVIL` to standard output if the log contains ANY anomalies.
5. Print exactly `CLEAN` to standard output if the log contains NO anomalies.
6. Exit with code 0.

To validate your script locally, you are provided two corpora:
- `/app/corpus/clean/`: Contains 20 CSV files with normal operations.
- `/app/corpus/evil/`: Contains 20 CSV files with injected anomalies.

Your script will be tested against a hidden, much larger corpus of clean and evil files. It must correctly classify 100% of both corpora.
You are an MLOps engineer tracking artifacts for a computer vision physics experiment. We have recorded a moving object, but our tracking system occasionally produces corrupted data with severe outliers and missing values. 

Your objective is to build a robust, reproducible data extraction and validation pipeline using `bash` and `C`.

**Phase 1: Video Data Extraction**
We have a video artifact of the experiment located at `/app/experiment.mp4`.
1. Use `ffmpeg` to extract the frames of this video as grayscale PGM (Portable GrayMap) images into `/home/user/frames/`.
2. Write a C program, `extract_tracking.c`, that reads a sequence of PGM files and calculates the (x, y) coordinates of the brightest pixel in each frame. 
3. The program should output a CSV file at `/home/user/extracted_trajectory.csv` with columns: `frame_id,x,y`.

**Phase 2: Artifact Sanitizer (Adversarial Corpus)**
Previous experiments have generated large amounts of tracking data, but some CSVs are corrupted due to sensor glitches (resulting in missing values, e.g., `-1,-1`, or impossible physics, e.g., the object teleporting more than 20 pixels between consecutive frames). 
1. We have provided two directories of historical tracking data artifacts:
   - `/app/corpora/clean/`: Contains 50 CSVs of valid, smooth trajectories.
   - `/app/corpora/evil/`: Contains 50 CSVs of corrupted trajectories (containing extreme outliers or missing values).
2. Write a C program, `artifact_filter.c`, that reads a CSV tracking file and determines if it is "CLEAN" or "EVIL" based on simple mathematical heuristics (handling missing values and detecting velocity outliers).
3. Create a bash script, `/home/user/pipeline.sh`, that acts as the entry point. It must accept a directory path as an argument, iterate through all CSV files in that directory, run your compiled `artifact_filter` on each, and print the filename and classification result in the format: `filename: CLEAN` or `filename: EVIL`.

**Phase 3: Hyperparameter Tuning**
Your filter needs a specific velocity threshold to distinguish clean data from outliers. Write an automated loop in your pipeline script that tests threshold values between 5 and 30, and configures your C program to use the hyperparameter that correctly preserves 100% of the clean corpus and rejects 100% of the evil corpus.

Ensure your code is reproducible, compiles with standard `gcc` (no external libraries other than the C standard library), and properly handles edge cases in file parsing.
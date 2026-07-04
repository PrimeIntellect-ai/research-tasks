You are an MLOps engineer responsible for setting up an artifact tracking and validation pipeline for physics-based machine learning experiments. You need to implement two components to ensure the reproducibility and schema consistency of our experiment tracking system.

**Component 1: Experiment Video Artifact Tracker**
Every experiment run generates a video artifact. You have been provided with a sample video at `/app/experiment_run.mp4`. 
Your task is to analyze this video by writing a C program (`/home/user/frame_analyzer.c`) and using standard CLI tools (like `ffmpeg`).
1. Extract all frames from `/app/experiment_run.mp4` into standard Portable GrayMap (PGM) format (`.pgm`, specifically the raw P5 format) using `ffmpeg`.
2. Your C program must read these PGM files, calculate the exact integer average grayscale pixel intensity for each frame (sum of all pixel values divided by total pixels, truncated to an integer).
3. The pipeline must generate a CSV file at `/home/user/video_metrics.csv` with the header `frame_number,avg_intensity` followed by the data (frames 1-indexed, sorted chronologically).

**Component 2: Hyperparameter Schema Validator**
To prevent tracking failed experiments, we need a strict schema enforcer for our hyperparameter configuration files. 
Write a C program (`/home/user/meta_validator.c`) that parses a configuration file and determines if it is valid. 
Compile this program to `/home/user/meta_validator`.

The program must take a single command-line argument: the path to a metadata file.
The metadata files contain key-value pairs (one per line, separated by `=`). 
A file is ONLY valid if it meets ALL the following schema rules:
- `learning_rate`: Must be a float strictly greater than 0.0 and less than or equal to 1.0.
- `batch_size`: Must be an integer that is exactly one of: 8, 16, 32, 64, 128, 256.
- `cv_folds`: Must be an integer between 2 and 10 (inclusive).
- If any key is missing, or if any unknown keys exist, the file is invalid.
- If the file cannot be opened, it is invalid.

Your program must exit with status code `0` if the file is perfectly valid, and a non-zero exit code (e.g., `1`) if the file is invalid. We will evaluate your compiled `meta_validator` binary against a large suite of valid and corrupted configurations.

Ensure your code is robust, strictly handles file I/O in C, and parses strings securely.
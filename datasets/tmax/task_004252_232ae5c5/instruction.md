You are tasked with a multi-stage data analysis and ETL pipeline to process dashcam footage and sensor data, and to build a data-quality filter for our reporting system.

**Stage 1: Video Analysis & Model Reconstruction**
We have a video file located at `/app/dashcam.mp4` (30 frames per second). 
You need to extract the frames from this video. We have a proprietary PyTorch model used to score each frame for visibility. The model weights are at `/app/model/weights.pth`, and a partial architecture is provided in `/app/model/arch.py`. The architecture file is missing some layer dimensions; you must reconstruct the correct input/output channels to successfully load the state dictionary.
Write a script to process the video, run inference on every frame (converted to grayscale, resized to 64x64, normalized to [0, 1]), and generate a CSV at `/home/user/frame_scores.csv` with columns: `frame_index`, `timestamp_sec`, `visibility_score`.

**Stage 2: Data Joining**
We have two CSV files: `/app/data/telemetry.csv` and `/app/data/gps.csv`.
Create an ETL script that joins these files with your `frame_scores.csv` on the closest `timestamp_sec`. Output the merged dataset to `/home/user/merged_data.csv`.

**Stage 3: Data Quality Filter (Plot Validation)**
Our automated reporting system generates matplotlib plots, but due to a backend misconfiguration, it sometimes produces blank or degenerate plots (e.g., solid white images, solid black images, or images with just axes and no data lines).
You must write a Python script `/home/user/filter_plots.py` that acts as a classifier. 
It must accept a single command-line argument (a directory path):
`python /home/user/filter_plots.py <directory_path>`
It should iterate through all `.png` files in the given directory and print a classification to standard output in the exact format:
`<filename>: ACCEPT` (for valid, data-containing plots)
`<filename>: REJECT` (for blank, solid, or misconfigured plots)

Your script will be tested against a hidden adversarial corpus of "evil" (glitched/blank) plots and a "clean" corpus of valid plots. To pass, it must correctly REJECT 100% of the evil corpus and ACCEPT 100% of the clean corpus.
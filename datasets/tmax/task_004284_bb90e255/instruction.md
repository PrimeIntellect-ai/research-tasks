You are a data engineer tasked with building an ETL pipeline to process video feeds from a factory floor. Your goal is to extract frames from a video, filter out corrupted or "glitch" frames caused by transmission errors, and calculate an anomaly probability metric for the valid frames.

You must implement this pipeline primarily in Bash. You may use standard Linux utilities (e.g., `awk`, `grep`, `imagemagick`, `ffmpeg`).

Here are the requirements:

1. **Adversarial Frame Filter:**
   A set of sample frames has been provided to you.
   - Clean frames (normal factory operations) are located in `/app/training_data/clean_corpus/`.
   - Evil frames (glitches, blackouts, transmission noise) are located in `/app/training_data/evil_corpus/`.
   
   Write a Bash script at `/home/user/detector.sh` that takes a single image file path as an argument. 
   - It must exit with code `0` if the image is clean.
   - It must exit with code `1` if the image is a glitch.
   Your script must correctly classify 100% of the files in both training directories. It will be tested against a hidden test corpus of clean and evil frames.

2. **Video ETL Extraction:**
   There is a video file located at `/app/factory_feed.mp4`.
   - Extract the frames from this video at exactly 1 frame per second (fps) as JPEG images into the directory `/home/user/extracted_frames/`. Name them as `frame_0001.jpg`, `frame_0002.jpg`, etc.
   
3. **Bayesian Anomaly Pipeline:**
   After extracting the frames, use your `/home/user/detector.sh` to process them. 
   - Discard (delete) any frames from `/home/user/extracted_frames/` that your detector classifies as glitches.
   - For the remaining valid frames, write an ETL script at `/home/user/pipeline.sh` that calculates a running Bayesian probability of a machine fault. 
   - The prior probability of a fault is `P(Fault) = 0.05`.
   - For each valid frame, analyze its average brightness (using ImageMagick). If the brightness is strictly less than 100 (on a 0-255 scale), treat it as an "Observed Event". If it is 100 or greater, treat it as "No Event".
   - `P(Event | Fault) = 0.8`
   - `P(Event | No Fault) = 0.1`
   - Calculate the posterior probability for each valid frame sequentially.

4. **Reporting:**
   Your pipeline must output a CSV file at `/home/user/etl_report.csv` with the following format:
   `frame_filename,is_glitch,brightness,fault_probability`
   - `frame_filename`: The name of the file (e.g., `frame_0001.jpg`). Include ALL original extracted frames.
   - `is_glitch`: `1` if detected as glitch by your script, `0` otherwise.
   - `brightness`: The integer average brightness (0-255). If it's a glitch frame, output `NA`.
   - `fault_probability`: The running posterior probability (rounded to 4 decimal places). If it's a glitch frame, output the last known probability.

Execute your pipeline so that `/home/user/etl_report.csv` is fully generated.
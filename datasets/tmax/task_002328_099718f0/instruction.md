You are an AI assistant helping a data scientist clean a multimodal dataset containing video recordings and corresponding text transcripts. The video pipeline suffered a backend misconfiguration (similar to an unconfigured matplotlib backend) which resulted in periodic completely blank (solid black) frames. Furthermore, the text transcripts have been targeted by a data poisoning attack.

You must build a reproducible pipeline using bash, Python, and R to clean this data and compute robust statistics.

**Step 1: Video Frame Analysis (Python & Bash)**
There is a video file located at `/app/experiment_record.mp4`.
1. Extract all frames from this video using `ffmpeg`.
2. Analyze the frames to detect "blank" frames. A frame is considered blank if the standard deviation of its pixel intensities (across all channels) is less than 2.0.
3. Compute the exact count of blank frames and the total number of frames.

**Step 2: Hypothesis Testing (R)**
Using the counts from Step 1, write an R script to compute the 95% Wilson score confidence interval for the proportion of blank frames.
Save the results in a JSON file at `/home/user/video_analysis.json` with the following exact keys:
- `"total_frames"`: (integer)
- `"blank_frames"`: (integer)
- `"ci_lower"`: (float, rounded to 4 decimal places)
- `"ci_upper"`: (float, rounded to 4 decimal places)

**Step 3: Adversarial Corpus Filtering (Python)**
We have discovered that some text transcripts have been poisoned. You must write a robust text filtering script.
Create a Python script at `/home/user/filter_transcripts.py` that takes two arguments:
`python3 /home/user/filter_transcripts.py <input_directory> <output_directory>`
The script should read all `.txt` files in the `<input_directory>`. For each file, it must:
1. Tokenize the text (split by whitespace).
2. Compute a simple character-level or token-level statistical embedding (e.g., TF-IDF or character frequency vectors).
3. Identify "evil" transcripts. Evil transcripts are characterized by a highly anomalous token-to-special-character ratio, or specific repetitive prompt-injection-like patterns (e.g., hidden Unicode blocks or anomalous punctuation density > 15%).
4. If a file is "clean", copy it to the `<output_directory>`. If it is "evil", drop it (do not output it).

To help you develop this, we have provided training samples at:
- `/app/training_corpus/clean/`
- `/app/training_corpus/evil/`

**Step 4: Pipeline Reproducibility**
Write a bash script `/home/user/run_pipeline.sh` that executes the full pipeline end-to-end (extracting frames, running the Python frame analysis, running the R script to produce the JSON, and running the transcript filter on a hypothetical `/app/test_corpus/`).

Ensure all scripts have the correct execution permissions and are fully self-contained. Do not rely on external API calls.
You are an ML engineer preparing a speech recognition dataset. Your pipeline needs to process raw audio, extract speech segments, and generate a perfectly formatted training manifest.

We have a 16kHz mono audio file located at `/app/interview.wav`. We also have the source code for `whisper.cpp` cloned at `/app/whisper/`, and a model file at `/app/ggml-tiny.en.bin`.

Your task is to write a reproducible Bash pipeline to generate a precise training manifest.

Step 1: Setup the Analysis Environment
Build `whisper.cpp` from source in its directory. You only need the main executable.

Step 2: Generate Transcripts
Run the whisper executable on `/app/interview.wav` using the provided model. Force it to output a CSV file containing the timestamps and text.

Step 3: Prepare the Training Data (The Pipeline)
Write a Bash script at `/home/user/build_manifest.sh` that takes the generated CSV file as input and produces a TSV (Tab-Separated Values) file at `/home/user/dataset.tsv`.

The output `/home/user/dataset.tsv` must have exactly these columns (with a header row):
`segment_id` | `start_ms` | `end_ms` | `duration_ms` | `transcript`

Data Constraints:
- `segment_id`: An integer starting at 1 for the first segment.
- `start_ms` / `end_ms`: Integer millisecond timestamps (extracted directly from the Whisper CSV).
- `duration_ms`: The exact duration of the segment in milliseconds (`end_ms - start_ms`). You must compute this!
- `transcript`: The transcribed text, stripped of leading/trailing whitespace.

WARNING: The whisper CSV output contains commas inside the transcribed text (which is quoted). A naive `awk -F','` or `cut` will silently corrupt your numeric columns and misalign the data, leading to invalid `duration_ms` calculations (akin to silent NaN introduction in Pandas). Your Bash script must robustly parse the CSV, handling quoted text correctly. Do NOT use Python, Ruby, or Perl. You must solve this using pure Bash, `awk`, `sed`, or other standard coreutils.

Deliverable:
Run your script so that `/home/user/dataset.tsv` is fully generated. Automated tests will evaluate the Mean Absolute Error (MAE) of your `duration_ms` column against the ground truth.
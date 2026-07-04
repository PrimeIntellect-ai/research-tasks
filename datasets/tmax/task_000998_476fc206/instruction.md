You are an MLOps engineer tasked with cleaning up a large-scale experiment artifact storage system. A recent batch of automated speech-to-text experiments generated thousands of CSV log files, but many of them are corrupted with missing values or outlier metrics due to a cluster failure.

Your goal is to build a robust Bash-based ETL filter that identifies and preserves valid experiment logs while discarding corrupted ones. 

First, you need to determine the correct outlier threshold for experiment duration. The lead researcher left an audio note at `/app/audio/researcher_note.wav`. Since we are operating in a terminal environment without a full speech recognition model, the researcher thoughtfully embedded the transcription directly into the audio file's metadata. 
1. Use standard multimedia tools (like `ffprobe`) to extract the `comment` or `title` metadata from the WAV file.
2. Parse this metadata to find the exact maximum allowed duration (in seconds) for a valid experiment.

Next, create an ETL filtering script at `/home/user/etl_filter.sh`. 
The script must meet the following specifications:
- **Signature:** `./etl_filter.sh <input_dir> <output_dir>`
- **Functionality:** It should iterate over all `.csv` files in `<input_dir>`. If a file is completely valid, copy it to `<output_dir>`. If a file contains ANY invalid data rows, discard the entire file (do not copy it).
- **Input Format:** Each CSV file has a header `id,duration,loss,wer` followed by one or more data rows.
- **Validation Rules (a row is valid ONLY IF):**
  1. **No Missing Values:** Every row must have exactly 4 columns. None of the fields can be empty.
  2. **Valid Duration:** The `duration` field must be a positive number (strictly greater than 0) and LESS THAN OR EQUAL TO the maximum duration threshold you extracted from the audio artifact.
  3. **Valid Loss:** The `loss` field must be a valid number greater than or equal to 0.
  4. **Valid WER:** The `wer` (Word Error Rate) field must be a valid number between 0 and 100 (inclusive).
- **Implementation Constraints:** 
  - Write the script entirely in Bash. You may use standard Unix utilities (e.g., `awk`, `sed`, `grep`, `coreutils`). `awk` is highly recommended for floating-point comparisons.
  - Make sure the script is executable (`chmod +x`).
  - Do not hardcode the threshold; you must read it from the audio file's metadata dynamically within your script, or you can hardcode the specific number you manually found from the audio file, but it must be exactly correct.

Your script will be tested against two hidden corpora:
1. A "clean" corpus of perfectly valid experiment logs. Your script MUST preserve 100% of these files.
2. An "evil" corpus of corrupted logs containing missing values, malformed data, and subtle outliers. Your script MUST reject 100% of these files.
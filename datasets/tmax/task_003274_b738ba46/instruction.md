You are a data scientist tasked with cleaning a corrupted multimodal dataset. 

You have two raw files in your workspace:
1. `/app/dataset/metadata_dirty.csv`: A CSV file containing transcript metadata. This file is corrupted. It contains duplicate rows, and some rows have been mangled with embedded newlines inside the 'text' column, causing them to span multiple lines silently.
2. `/app/dataset/raw_recording.wav`: A raw audio recording at 48kHz stereo, which contains several long gaps of absolute silence.

Your goal is to use Bash shell commands and standard Linux utilities (like `awk`, `sed`, `grep`, `ffmpeg`, etc.) to clean and normalize these assets.

Perform the following steps:
1. **Clean the CSV Dataset**:
   Process `/app/dataset/metadata_dirty.csv` and write the output to `/home/user/metadata_clean.csv`.
   - Reconstruct the rows that were split by embedded newlines (assume every valid row must start with an integer ID and a timestamp, e.g., `101,00:01:22,...`). 
   - Tokenize and normalize the 'text' column by converting all characters to lowercase.
   - Deduplicate the rows based on the exact hash of the normalized text column. Keep only the first occurrence of any duplicate text.

2. **Process and Resample the Audio**:
   Process `/app/dataset/raw_recording.wav` using `ffmpeg` and save it to `/home/user/processed_audio.wav`.
   - Resample the audio to 16000 Hz.
   - Convert the audio to mono (1 channel).
   - Use an audio filter to strip out all silences longer than 1.0 second (leaving at most a 0.1-second gap where the silence was).

Work entirely in the terminal using Bash commands. Produce the exact file names requested above.
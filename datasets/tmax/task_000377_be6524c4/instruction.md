Hello, I am a researcher organizing a large catalog of datasets, and I need your help building a specific data processing pipeline. 

I recently recorded an audio memo detailing a manual "embedding" and dimensionality reduction strategy we are using to organize our dataset metadata. The recording is located at `/app/research_memo.wav`.

Your task is to:
1. Transcribe or listen to the audio memo to understand the specific feature engineering and encoding rules I requested. You can use standard tools like `ffmpeg` or `whisper.cpp` if installed, or any other command-line utilities you prefer to extract the spoken instructions.
2. Write a Python script at `/home/user/dataset_encoder.py` that implements this exact logic. 
3. The script must read a single JSON object representing a dataset's metadata from standard input (`stdin`).
4. The script must process the JSON according to the rules in the audio memo and print the resulting numerical vector to standard output (`stdout`) as a comma-separated string, followed by a newline.

The JSON input will always have the following keys:
- `dataset_name` (string)
- `num_rows` (integer)
- `is_public` (boolean)

Please ensure your Python script exactly matches the numerical transformations described in the audio. Your code will be rigorously tested against thousands of synthetic dataset records to ensure it behaves identically to our reference implementation.

Do not write any extra output or debug logs to `stdout`, as it will break the automated validation pipeline.
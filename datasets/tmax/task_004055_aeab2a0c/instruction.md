You are an AI assistant helping a data analyst debug a data pipeline and configure their environment. 

We are processing acoustic features into CSV files. Recently, we discovered a silent bug: some of our CSV files have missing values in strictly integer columns (`speaker_id` and `frame_index`). When pandas loads these, it silently converts the entire column from `int` to `float` (introducing NaNs), which subsequently crashes our C++ downstream inference tools that expect strict integers.

Your task has three parts:

1. **Environment Setup and Benchmarking**:
   - Install `pandas` and `librosa`. 
   - We have an audio file located at `/app/recording.wav`.
   - Write a short script to load this audio file using `librosa`, extract 13 MFCC features, and save the resulting feature matrix into a CSV at `/home/user/features.csv`. Configure your numerical backend (e.g., OpenBLAS) to use exactly 1 thread to simulate our single-threaded production environment. 

2. **Adversarial Sanitizer**:
   - We need a robust filter to protect the downstream C++ tools. Write a Python script at `/home/user/sanitizer.py` that takes exactly one command-line argument: the path to a CSV file.
   - The script must inspect the CSV. If the CSV is "clean", it must exit with code `0`. If the CSV is "evil" (corrupted), it must exit with code `1`.
   - **Clean CSVs**: The `speaker_id` and `frame_index` columns contain strictly integer representations (e.g., "5", "10").
   - **Evil CSVs**: The `speaker_id` or `frame_index` columns contain missing values (empty strings), NaNs, or floating-point representations (e.g., "5.0", "NaN", "").

Ensure your `/home/user/sanitizer.py` runs cleanly from the terminal and accurately catches the silent float/NaN conversions that pandas might otherwise mask.
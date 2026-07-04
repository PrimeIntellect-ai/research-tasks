You are a data scientist tasked with cleaning a large, corrupted telemetry dataset. The lead engineer left you an audio memo with specific instructions on how to handle the noise before calculating our baseline metrics. 

Your task involves several steps:
1. **Transcribe the Audio Memo**: There is an audio file located at `/app/audio_memo.wav`. You will need to install and use a local transcription tool (like `whisper.cpp` or `pocketsphinx`) to transcribe this audio file. The memo contains a crucial numerical threshold required for filtering the dataset.
2. **Build an ETL pipeline in C**: You have a massive raw binary file at `/app/sensor_data.bin`. This file contains exactly 1,000,000 records. Each record is a 10-dimensional vector of standard IEEE 754 double-precision floating-point numbers (80 bytes per record).
3. **Data Cleaning & Linear Algebra**: Write a C program, `process_telemetry.c` in `/home/user/`, that reads this binary file. For each 10-dimensional vector, calculate its Euclidean norm (L2 norm). If the norm is strictly greater than the threshold mentioned in the audio memo, the record is considered corrupted and must be discarded.
4. **Bootstrapping / Aggregation**: For the remaining "clean" vectors, compute the exact sample mean for each of the 10 dimensions. 
5. **Output**: Your C program must write the final 10-dimensional mean vector to a single line in `/home/user/result.csv`, with the values separated by commas. 

Requirements:
- Your core data processing logic must be written in **C**. You can use standard standard libraries and `math.h`.
- You are free to use bash commands to setup your environment, install transcription dependencies, and compile your code.
- Ensure your C code is highly efficient and handles large-scale data streamingly if necessary.
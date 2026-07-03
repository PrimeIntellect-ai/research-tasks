You are a bioinformatics systems analyst investigating a pipeline that processes gel electrophoresis video simulations and DNA signal traces. 

You have two main objectives:

**Part 1: Video Signal Extraction**
There is a simulated electrophoresis video located at `/app/electrophoresis.mp4`. 
1. Use `ffmpeg` and standard Bash CLI tools (like `awk`, `grep`, `bc`) to extract the frames from this video.
2. Calculate the average grayscale pixel intensity for each frame.
3. Identify the frame number (1-indexed, meaning the first frame is frame 1) that has the **maximum** average pixel intensity.
4. Save just the integer frame number to `/home/user/max_frame.txt`.

**Part 2: Adversarial Trace Filtering (Reproducible Computation)**
We discovered that some signal trace files from our sequencing machines are corrupted or tampered with. Because floating-point addition is not strictly associative, naive summations of these trace files previously masked the tampering. We have defined a strictly reproducible summation protocol to verify file integrity.

A trace file is structured with a header line `# SUM: <value>` followed by multiple lines of floating-point intensity values.
A trace is considered **VALID (clean)** if and only if:
When the intensity values (excluding the header) are sorted numerically in strictly **descending** order, and then summed sequentially (one by one, top to bottom) using exactly 4 decimal places of precision (e.g., using `bc` with `scale=4`), the resulting sum exactly matches the `<value>` in the header.
A trace is **INVALID (evil)** if the sum does not match, or if it contains malformed data.

You have been provided two directories to test your logic:
- `/app/corpus/clean/` (contains valid traces)
- `/app/corpus/evil/` (contains tampered/invalid traces)

Write a Bash script at `/home/user/sanitizer.sh` that takes a single file path as an argument.
- The script must `exit 0` if the trace file is VALID.
- The script must `exit 1` if the trace file is INVALID.

Your script must perfectly separate the clean and evil files. Do not use Python; rely entirely on Bash built-ins, coreutils, `bc`, `awk`, `sed`, etc.
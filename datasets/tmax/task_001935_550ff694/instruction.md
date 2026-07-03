You are a performance engineer tasked with processing acoustic profiling data and building a robust validation pipeline for application traces.

Your objective has three parts:

**Part 1: Acoustic Data Extraction**
We received an audio memo from the lead engineer detailing the baseline latency calibration matrix. The audio file is located at `/app/baseline_memo.wav`. You must transcribe this audio file to recover the spoken baseline values. Write the exact numerical values mentioned in the audio into a file called `/home/user/baseline.txt` (one number per line, in the order they were spoken). You may install and use any transcription tools (like whisper.cpp or ffmpeg) necessary to process the audio.

**Part 2: Trace Reshaping and Graph Processing**
Application traces are being exported as JSON files containing a list of function calls. Each call object has:
- `id` (string)
- `parent_id` (string, empty if root)
- `duration_ns` (float64)
- `invocations` (int)

You need to write a Go program (`/home/user/trace_analyzer.go`) that reconstructs the call graph from these objects (reshaping the observational data into a tree/graph structure). The program must calculate the "effective operation cost", defined as `duration_ns / invocations`.

**Part 3: Adversarial Corpus Filtering (Numerical Stability & Graph Validation)**
Because our trace collectors sometimes malfunction, they produce corrupt ("evil") traces. You must write a Go-based filter CLI tool at `/home/user/trace_filter.go`. 

This tool must accept a single argument (the path to a trace JSON file) and exit with code `0` if the trace is valid, or exit with code `1` if the trace is invalid.

A trace is **invalid** ("evil") and must be rejected if ANY of the following are true:
1. **Graph Anomaly:** The call graph contains a cycle (e.g., function A calls B, which calls A).
2. **Numerical Instability:** Any calculation of `duration_ns / invocations` would result in a division by zero, Infinity, or NaN.
3. **Data Corruption:** Any `duration_ns` is less than 0.

A trace is **valid** ("clean") if it forms a valid directed acyclic graph (tree/forest) and all calculated costs are finite, positive, and numerically stable.

To help you develop your filter, we have provided two directories:
- `/app/corpus/clean/`: Contains strictly valid trace JSON files.
- `/app/corpus/evil/`: Contains strictly invalid trace JSON files.

**Success Criteria:**
1. `/home/user/baseline.txt` contains the correct transcribed numbers.
2. You have compiled your filter to `/home/user/trace_filter`.
3. Your compiled filter must successfully exit 0 for **100%** of the files in `/app/corpus/clean/`.
4. Your compiled filter must successfully exit 1 (or non-zero) for **100%** of the files in `/app/corpus/evil/`.

Ensure your Go code is well-structured and properly handles the numerical edge cases.
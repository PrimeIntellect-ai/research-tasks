You are acting as an AI assistant for a research scientist organizing a large-scale sensor dataset.

The researcher has left a workspace with raw data and an audio dictation memo. Your goal is to figure out the specific filtering rules from the audio memo, inspect the raw data structure, and write a high-performance C++ parser that implements the requested filtering.

Here are the specific steps you must follow:

1. **Audio Transcription**
   There is an audio recording of the researcher's latest field notes at `/app/filter_memo.wav`. The researcher dictates the exact filtering criteria for the dataset in this audio. 
   You must transcribe this audio to find out the rules. A pre-compiled version of Whisper is available at `/opt/whisper.cpp/main` along with the English base model at `/opt/whisper.cpp/models/ggml-base.en.bin`. 

2. **Data Inspection (Shell and Text Tools)**
   The raw dataset samples are located in a deeply nested archive at `/app/sensor_logs.tar.gz`. This archive contains nested tar, zip, and gzip files. You should use shell commands (`tar`, `unzip`, `find`, `zcat`, `awk`, `sed`) to recursively explore these archives and understand the format of the multi-line log records. 
   Notice the multi-line structure: records have fields like `EventID`, `Severity`, `Temperature`, `Battery`, etc., and are separated by a delimiter line consisting of exactly three dashes (`---`).

3. **C++ Parser Implementation**
   Write a C++ program at `/home/user/parser.cpp` and compile it to an executable at `/home/user/parser`.
   The program must read raw, multi-line log text from standard input (`stdin`) until EOF.
   It must parse the multi-line records and apply the exact filtering logic dictated in the audio memo.
   For each record that matches the criteria, output the specific fields requested in the audio memo, formatted exactly as requested, to standard output (`stdout`), with one matched record per line.
   Do not output anything else to stdout (no debugging information, no headers).

Your compiled program `/home/user/parser` will be tested rigorously with thousands of randomly generated log streams to ensure it perfectly matches the researcher's reference implementation.
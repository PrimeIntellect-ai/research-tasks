I need you to build a small utility pipeline to extract and analyze audio features. 

We have a directory `/app/extractor` containing the source code for a C utility that reads a standard WAV file and outputs a raw binary file of power levels. However, the C program has a couple of compilation issues, and its `Makefile` is broken. 

Your tasks are:
1. Fix the `Makefile` and any compilation errors in `/app/extractor/main.c`.
2. Compile the C program to an executable named `extract_features`.
3. Run the executable on the provided audio file at `/app/signal.wav` to produce a binary output file at `/app/extractor/features.bin`.
4. Write a Go program at `/app/process.go` that reads `features.bin`. The binary file contains a sequence of 8-byte records (Little Endian):
   - A `uint32` representing the timestamp in milliseconds.
   - A `float32` representing the RMS power level.
5. In your Go program, implement a simple moving average (SMA) filter on the power levels with a window size of 5 records (the filtered value at index `i` is the average of indices `i-2` to `i+2`, handling edges by truncating the window).
6. Find all local maxima in the smoothed power levels where the smoothed power is strictly greater than `0.5`. A local maximum is defined as a point strictly greater than its immediate neighbors.
7. Output the detected peaks as a JSON array of objects to `/app/peaks.json`, with the following structure:
   ```json
   [
     {"time_ms": 105, "smoothed_power": 0.812},
     ...
   ]
   ```
   Save the output to `/app/peaks.json`.

Ensure your Go code is well-structured and performs the serialization and deserialization correctly. Do not modify the underlying audio file.
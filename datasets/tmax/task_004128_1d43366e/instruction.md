I am a researcher organizing a massive dataset of bio-acoustic recordings. I have a continuous, multi-gigabyte raw 16-bit PCM audio stream located at `/app/dataset_stream.raw` (headerless, 44100Hz, 1 channel). 

I need you to write a highly efficient C++ program that can extract arbitrary slices from this large file, apply a volume scaling transformation, and save them atomically. Due to the file size, you **must** use memory-mapped I/O (`mmap`) to read the input file. To prevent dataset corruption from interrupted batch jobs, all file writes must be atomic (write to a temporary file in the same directory, then rename it to the final target path).

Write your C++ code to `/home/user/dataset_tool.cpp` and compile it to `/home/user/dataset_tool`.

The program must run continuously, reading instructions from standard input, one per line.
Each instruction will have the format:
`extract <offset_bytes> <length_bytes> <scale_factor> <output_path>`

For each instruction, your program should:
1. Extract `length_bytes` starting from `offset_bytes` in `/app/dataset_stream.raw`. (Assume the offset and length are always even numbers, aligning with 16-bit samples).
2. Treat the extracted bytes as signed 16-bit little-endian integers. Multiply each sample by the float `scale_factor`.
3. Clamp the resulting values to the valid range of a signed 16-bit integer (-32768 to 32767).
4. Atomically write the scaled raw PCM bytes to `output_path`. (Create a temporary file named `<output_path>.<random_or_pid>.tmp`, write the data, and use `rename()` to move it to `output_path`).
5. Print "DONE <output_path>" to standard output.
6. Flush standard output so the caller knows the file is ready.

You must handle paths correctly (the output directory might be different from the current working directory). The program should exit cleanly when EOF is reached on standard input. 

I will test your tool against a reference implementation using thousands of random extraction requests to ensure it is bit-exact and handles system I/O correctly.
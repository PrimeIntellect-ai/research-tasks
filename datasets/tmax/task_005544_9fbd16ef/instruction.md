I am a researcher organizing a massive, messy dataset of sensor readings, and I need your help to process it efficiently. 

In `/home/user/dataset/raw/`, there is a deeply nested directory structure containing hundreds of sensor data files. The files come in two formats:
1. `*.bin` files: Binary files containing exactly 10 double-precision floats (80 bytes total) in little-endian format.
2. `*.tsv` files: Text files containing 10 tab-separated floating-point numbers on a single line.

I need you to write a C++ program and use shell commands to process these files concurrently and consolidate the results.

Here is what you need to do:
1. Write a C++ program at `/home/user/process_sensor.cpp` and compile it to `/home/user/process_sensor`.
2. The C++ program must:
   - Accept a format flag (`--bin` or `--tsv`) as the first argument, and the original file path as the second argument.
   - Read the 10 data points from **standard input (stdin)**.
   - Calculate the arithmetic mean of the 10 values.
   - Append a line to `/home/user/dataset/master_index.csv` in the format: `[original_file_path],[mean_value_formatted_to_4_decimal_places]` (e.g., `/home/user/dataset/raw/a/sensor.bin,12.3456`).
   - **Crucially:** Because we will run this in parallel, your C++ program *must* use POSIX file locking (`flock()` or `fcntl()`) on `master_index.csv` to ensure concurrent writes are not corrupted or interleaved. 

3. Once compiled, use a combination of `find`, standard standard input redirection (`<`), and `xargs` to process all `*.bin` and `*.tsv` files in `/home/user/dataset/raw/` concurrently using exactly 8 parallel processes. 
   - For example, you should pipe the paths from `find` into `xargs -P 8` and redirect the file contents into the standard input of your C++ executable.

When you are done, the file `/home/user/dataset/master_index.csv` should contain exactly one line for every file in the raw dataset, correctly formatted and uncorrupted by race conditions.
You are an ML engineer tasked with preparing a large-scale embedding dataset for training. Our legacy pipeline uses a proprietary, highly optimized C binary to perform custom dimensionality reduction and quantization on high-dimensional data before storing it in our experiment tracking backend. 

Unfortunately, the source code for this specific data transformation tool was lost, and we only have a stripped compiled binary located at `/app/dim_reducer_oracle`. 

We need to migrate our systems, and to do so, we must reimplement the exact same algorithm in C. Your task is to reverse-engineer the behavior of `/app/dim_reducer_oracle` (you can use tools like `objdump`, `gdb`, or treat it as a black-box oracle by observing input/outputs) and write a drop-in replacement C program.

The binary reads from standard input and writes to standard output.
Input format: 
- A 32-bit unsigned integer `N` representing the number of vectors.
- Followed by `N` vectors. Each vector consists of 128 `float` values (512 bytes per vector).

Output format:
- For each of the `N` input vectors, the program outputs a reduced vector of 16 `uint8_t` values.

You must write your C code in `/home/user/dim_reducer.c` and compile it to `/home/user/dim_reducer`. Your compiled binary must be BIT-EXACT equivalent to `/app/dim_reducer_oracle` for any valid input.
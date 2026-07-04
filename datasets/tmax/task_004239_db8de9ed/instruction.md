You are assisting a bioinformatics analyst. We are working with a large dataset of sequence binding affinities, but we've run into an issue: our previous simulations produced non-reproducible and inaccurate results due to floating-point reduction order and precision loss when summing millions of single-precision floats.

We have a binary data file located at `/home/user/data/affinities.bin`. It contains exactly 1,000,000 single-precision floating-point numbers (`f32` in little-endian format). 

Your task is to write a Rust program `/home/user/compute_integral.rs` that reads this binary file and performs a numerically stable numerical integration (cumulative sum) using the **Kahan summation algorithm**. Using standard `+=` will result in significant precision loss, which is exactly what we are trying to avoid.

The program must calculate the running integral (cumulative sum) across all 1,000,000 values using Kahan summation.

Your Rust program should write its output to `/home/user/results.txt` with the following specific format:
- Line 1: The total sum of all 1,000,000 elements, formatted to 4 decimal places.
- Lines 2 to 11: The running sum at every 100,000th element. Specifically, print the cumulative sum at indices `99,999`, `199,999`, `299,999`, ..., `999,999` (using 0-based indexing), each on a new line and formatted to exactly 4 decimal places.

Compile and execute your Rust program so that `/home/user/results.txt` is generated successfully.
You are a performance engineer tasked with modernizing a critical bottleneck in our satellite data processing pipeline. 

The bottleneck is an old, undocumented, stripped binary located at `/app/astro_filter`. This binary processes extracted time-series data from our FITS files. It reads raw double-precision floating-point numbers (`f64`, little-endian) from standard input until EOF, and outputs exactly two double-precision floating-point numbers (`f64`, little-endian) to standard output. 

From historical notes, we know this binary computes the **mean** and the **sample variance** of the input dataset. Because the satellite data often has a very large baseline offset, a naive "sum of squares" approach suffers from catastrophic cancellation and floating-point drift. The original author used a numerically stable algorithm to compute these statistics in a single pass.

Your task:
1. Treat `/app/astro_filter` as a black box (or reverse-engineer it using tools like `xxd`, `objdump`, or `strace` if you wish) to confirm its behavior.
2. Create a high-performance, bit-exact equivalent of this tool in Rust.
3. Initialize your Rust project at `/home/user/astro_fast`.
4. Ensure your implementation also avoids catastrophic cancellation by using the correct numerically stable algorithm, matching the binary's output exactly (bit-for-bit on the `f64` outputs).
5. Compile your project in release mode so the final executable is located at `/home/user/astro_fast/target/release/astro_fast`.

Your Rust executable must accept the identical binary stream on stdin and produce the identical binary stream on stdout.
You are a security researcher analyzing a newly discovered, mysterious Linux executable named `suspicious_bin` located in `/home/user/`. 

When run, the binary quietly exits, but static analysis suggests it relies on a hidden Write-Ahead Log (WAL) file dropped elsewhere on the filesystem to execute its true payload. The binary calculates a cryptographic key based on an iterative sequence of floating-point values stored in this WAL file.

You have a preliminary Rust script, `/home/user/recover.rs`, designed to parse the WAL and calculate the decryption key. However, it currently produces wildly inaccurate outputs and fails to converge to the correct key.

Your task is to:
1. Use system call tracing on `/home/user/suspicious_bin` to locate the exact path of the hidden WAL file it attempts to open.
2. The WAL file contains a corrupted 4-byte header that must be skipped. The rest of the file consists of a continuous stream of 32-bit little-endian floats.
3. Fix the `recover.rs` script. The sequence relies on a telescoping product. Due to the high number of iterations, the current code suffers from severe precision loss, causing convergence failure. You must upgrade the accumulation logic to use double precision (`f64`) to calculate the exact key, while correctly reading the initial 32-bit floats.
4. Execute your fixed Rust script against the hidden WAL file.
5. Save the final calculated key (formatted to 5 decimal places, e.g., `12345.67890`) into `/home/user/key.txt`.

Ensure your final `key.txt` contains only the recovered numerical key.
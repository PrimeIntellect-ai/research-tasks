You are an engineer tasked with fixing a multi-file Rust project that currently fails to compile due to broken mathematical constants and corrupted files. You will write a single Python script `/home/user/fix_project.py` to automate the entire recovery, patching, code generation, and benchmarking process.

The project is located at `/home/user/rust_proj/`. 
You need to accomplish the following using your Python script:

1. **Decode and Apply Patch**: 
   A co-worker left a patch to fix `/home/user/rust_proj/src/math_ops.rs`, but the patch file itself was corrupted during transfer. The corrupted patch is at `/home/user/encoded_patch.txt`. 
   Every line in this file starts with `ENC: ` followed by a Hex-encoded string. Your script must read this file, extract and decode the Hex data into UTF-8 text to reconstruct a standard Unified Diff. Then, your script must apply this diff to `/home/user/rust_proj/src/math_ops.rs`. You may use Python's standard libraries or invoke the system `patch` command from within your script.

2. **Mathematical Code Generation**:
   The file `/home/user/rust_proj/src/constants.rs` is missing. Your script must calculate the first 100 prime numbers (where 2 is the first prime, 3 is the second, etc.) and generate this file. The generated Rust file must contain exactly this definition, formatting the array properly:
   ```rust
   pub const PRIMES: [u32; 100] = [2, 3, 5, 7, /* ... remaining primes ... */];
   ```

3. **Performance Benchmarking**:
   Because the Rust compiler (`rustc`) might not be fully configured in this isolated environment, we have provided a Python replica of the compiled binary at `/home/user/rust_proj/mock_rust_binary.py`. 
   Your script must benchmark this replica. The replica takes a single integer argument (e.g., `python mock_rust_binary.py 100`). 
   Benchmark the script for the inputs `10`, `100`, and `1000`. For each input, measure the wall-clock execution time (in seconds) of the process. 
   Save the results to `/home/user/benchmark.json` in the following exact JSON structure:
   ```json
   {
     "10": 0.0012,
     "100": 0.0125,
     "1000": 0.1301
   }
   ```

Write and execute `/home/user/fix_project.py` to perform these actions. Ensure the final `math_ops.rs` is patched, `constants.rs` is created with the correct primes, and `benchmark.json` is generated.
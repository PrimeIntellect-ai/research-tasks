You are an engineer tasked with porting a legacy C project to run inside a highly minimal Linux container. During the porting process, you discovered that the existing `Makefile` relies on external tools (`bc`, `sort -V`, `md5sum`, etc.) that are stripped from the target container. 

To bypass the linking and configuration errors, you need to write a standalone configuration script that replicates the missing build-prep steps using only Bash and standard Python 3 (which is guaranteed to be present).

Write a Bash script at `/home/user/build_prep.sh`. When executed, this script must perform the following tasks and output a configuration summary:

1. **Semantic Version Comparison**: The project depends on a specific library. A list of available library versions is located at `/home/user/deps/libs.txt`. Parse this file and determine the highest semantic version (ignoring build metadata but correctly ordering pre-release tags if any, though standard `X.Y.Z` comparison is the priority).
2. **Expression Evaluation**: The build requires setting a buffer size based on a mathematical formula stored in `/home/user/deps/config.expr`. Read and evaluate this mathematical expression (it contains standard basic arithmetic operators like `+`, `-`, `*`, `/`).
3. **Checksum / Integrity**: The build requires verifying a static asset at `/home/user/deps/payload.dat`. Calculate the Adler-32 checksum of this file. Output the checksum as an 8-character zero-padded lowercase hexadecimal string.
4. **Performance Benchmarking**: The minimal environment has strict CPU limits. Write a small benchmark routine inside your script that computes the Adler-32 checksum of `payload.dat` exactly 10,000 times in a tight loop. Measure the total elapsed time of this loop in seconds (can be a floating-point value).

Your script must generate a log file exactly at `/home/user/prep_results.log` with the following key-value format:

```text
HIGHEST_VERSION: <the_highest_version>
BUFFER_SIZE: <evaluated_result>
PAYLOAD_ADLER32: <hex_checksum>
BENCHMARK_TIME: <elapsed_time_in_seconds>
```

Make sure your script is executable (`chmod +x /home/user/build_prep.sh`) and runs successfully. You may use Python 3 inline within your Bash script to handle complex logic like Adler-32 or semantic versioning if you prefer. Do not use external libraries outside of the Python standard library.
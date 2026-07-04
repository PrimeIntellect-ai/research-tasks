You are a data scientist working on cleaning and processing user text records. You need to build a highly performant, reproducible command-line pipeline that filters invalid records, computes a lightweight character "embedding" (a simple XOR hash), and joins the data with an existing legacy dataset. 

Because performance is critical, you must implement the core data processing tool in C and orchestrate the pipeline using standard bash utilities.

Here are the requirements:

1. **Write a C program (`/home/user/process.c`):**
   - The program should read comma-separated values from `stdin`. The format of the input will strictly be three columns: `id,email,raw_text`. There will be no commas inside the fields.
   - It must filter out (drop) any rows where the `email` field does not contain the `@` character.
   - For valid rows, it must compute a mock "embedding hash": the bitwise XOR sum of all ASCII characters in the `raw_text` field (excluding the newline character at the end).
   - The program should output to `stdout` in the format: `id,xor_hash`

2. **Create a bash pipeline script (`/home/user/run.sh`):**
   - The script must compile `/home/user/process.c` into an executable at `/home/user/process` using `gcc` with `-O3` optimization.
   - It should process the raw dataset located at `/home/user/data/users.csv` using the compiled `./process` executable.
   - It must benchmark the execution time of the `./process` command using the standard `/usr/bin/time` utility, writing the timing output to `/home/user/bench.txt`.
   - It must then sort the output by `id` (numerically) and use the standard bash `join` command to join the results with `/home/user/data/legacy_hashes.csv` (which is already sorted) on the `id` field.
   - The final joined dataset must be saved to `/home/user/final.csv`. The format should be `id,xor_hash,legacy_hash`.

Make sure the bash script has executable permissions and can be run independently to reproduce the entire pipeline.
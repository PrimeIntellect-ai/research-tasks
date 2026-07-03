You are an operations engineer investigating a faulty ETL pipeline that generates duplicate log records upon retry attempts. To accurately aggregate the data, you need to build a C-based deduplication filter that normalizes text tokens, aligns timestamps, and drops duplicate events. 

Your task is to write a highly efficient C program that acts as a standard UNIX filter (reading from `stdin`, writing to `stdout`). 

**Task Steps:**

1. **Fix the Vendored Library**: 
   We rely on the `uthash` library for efficient C-based hash maps. The source is vendored at `/app/uthash-2.3.0`. However, the previous maintainer made an incomplete patch to `/app/uthash-2.3.0/src/uthash.h` that causes compilation errors when using the string-key macros. Identify and fix the syntax error in `uthash.h` so it can be used in your program.

2. **Write the Deduplication Filter**:
   Create a C program at `/home/user/etl_dedup.c` and compile it to `/home/user/etl_dedup` (ensure you include `/app/uthash-2.3.0/src` in your include path).

   **Input Format:**
   Lines on `stdin` formatted exactly as:
   `YYYY-MM-DD HH:MM:SS|RAW_PAYLOAD\n`

   **Processing Rules:**
   - **Timestamp Parsing:** Convert the `YYYY-MM-DD HH:MM:SS` string (assumed to be in UTC) to a UNIX epoch integer.
   - **Tokenization & Normalization:** Process `RAW_PAYLOAD` to create a `NORMALIZED_PAYLOAD`. 
     - Convert all alphabetical characters to lowercase.
     - Strip all non-alphanumeric characters (remove punctuation, symbols, etc.), replacing them with a single space.
     - Trim leading and trailing whitespace, and collapse multiple consecutive spaces into a single space.
   - **Deduplication:** Track the `NORMALIZED_PAYLOAD`. If this exact normalized payload has *already* been seen in the stream, drop the record entirely (it is a retry duplicate). 

   **Output Format:**
   For every *novel* normalized payload, output exactly one line to `stdout`:
   `EPOCH_INTEGER|NORMALIZED_PAYLOAD\n`

3. **Orchestration**:
   Create a wrapper script at `/home/user/run_pipeline.sh` that takes an input file as `$1`, pipes it through `/home/user/etl_dedup`, and writes the output to `$2`.

Your compiled C binary will be rigorously tested against an automated fuzzing verifier that streams thousands of simulated ETL logs to your program's `stdin` and requires bit-exact output against our golden oracle. Ensure your C code has no memory leaks or buffer overflows.
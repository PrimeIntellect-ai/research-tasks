You are helping a data analyst build a high-performance data processing pipeline in C. The analyst has a large CSV dataset of text logs and needs to enforce a strict schema, compute a text fingerprint (acting as a simple embedding for fast retrieval), and store the valid records in a highly efficient binary format.

Your task is to write a C program (`/home/user/process.c`) and a pipeline script (`/home/user/run_pipeline.sh`) to perform this processing.

**Input Data:**
The input file is located at `/home/user/data.csv`. It has a header row and uses standard comma separation.
Columns: `id` (integer), `category` (string), `text` (string). 
You can assume no commas exist within the string fields themselves.

**Schema Enforcement Rules:**
You must parse each row and drop any row that violates the following rules:
1. `id` must be strictly greater than 0.
2. `category` must be exactly one of the following strings: "A", "B", or "C".
3. `text` must not be empty (length > 0).

**Fingerprint (Embedding) Computation:**
For every valid row, compute a 64-bit fingerprint of the `text` field using the FNV-1a hash algorithm.
* Algorithm specifics:
  * Initialize `hash` as an unsigned 64-bit integer to `14695981039346656037` (FNV offset basis).
  * For each byte `b` in the `text` string (excluding the null terminator or newline):
    * `hash = hash ^ (unsigned byte)b`
    * `hash = hash * 1099511628211` (FNV prime)

**Output Format:**
Write the valid records to a binary file at `/home/user/store.bin`.
The binary file should contain a sequence of tightly packed structs representing the valid rows, in the exact order they appeared in the CSV.

You must use the following C struct (ensure it is packed with no padding):
```c
#pragma pack(push, 1)
struct Record {
    int32_t id;
    char category[4]; // null-terminated string, padded with null bytes if less than 4 chars
    uint64_t fingerprint;
};
#pragma pack(pop)
```

**Pipeline Script:**
Create an executable bash script at `/home/user/run_pipeline.sh` that:
1. Compiles `/home/user/process.c` into an executable at `/home/user/process`. Use `gcc -O3`.
2. Runs `/home/user/process`.

Make sure to handle the CSV header properly (skip it). Your C program should read `/home/user/data.csv` and write to `/home/user/store.bin`.
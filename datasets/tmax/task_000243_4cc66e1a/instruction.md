You are a build engineer managing artifact uploads to a custom registry. You have been given a raw upload log file and a legacy C library used for computing artifact integrity hashes.

Your task is to write a Python script `/home/user/process_logs.py` that parses the log, filters out spam uploads via rate limiting, computes a hash using the provided C library, and outputs the valid records to a JSON file.

Here are the requirements:

1. **Input File:** You are provided with `/home/user/upload_logs.txt`. The log contains upload requests. You must parse this file using a state machine approach. The format is a sequence of blocks:
```
START_REQ
USER: <username>
TS: <timestamp_in_seconds>
SIZE: <file_size_bytes>
END_REQ
```
Note: Ignore any lines outside of the `START_REQ` and `END_REQ` blocks. A valid block will always contain USER, TS, and SIZE exactly once, but they may appear in any order. 

2. **Request Validation & Rate Limiting:** 
   - Requests must be processed in the order they appear in the file.
   - You must apply a rate limit: A user can only make a maximum of 2 *accepted* requests in any 60-second rolling window. 
   - Specifically, a request at timestamp `T` is accepted if the user has strictly fewer than 2 *previously accepted* requests in the inclusive time window `[T - 59, T]`.
   - Discard any requests that exceed this limit.

3. **FFI and Hashing (C library):**
   - You are provided with a pre-compiled shared library `/home/user/libhasher.so`.
   - It exposes a C function: `uint32_t compute_hash(const int32_t* data, int length)`.
   - For every *accepted* request, use Python's `ctypes` to call this function.
   - Pass an array of 2 integers containing the timestamp and the size, respectively (i.e., `data = [TS, SIZE]`, `length = 2`).

4. **Output:**
   - Write the accepted requests to `/home/user/processed_artifacts.json` as a JSON array of objects.
   - Each object must have exactly three keys: `"user"` (string), `"ts"` (integer), and `"hash"` (integer, the unsigned 32-bit output from the C function).
   - Order the JSON array in the exact order the accepted requests appeared in the input file.

Do not use any external Python libraries (only standard library modules like `ctypes`, `json`, etc., are permitted). You should execute your script to generate the output file.
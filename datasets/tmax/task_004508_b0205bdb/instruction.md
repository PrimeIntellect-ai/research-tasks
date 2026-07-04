You are tasked with fixing and completing a C++ data ingestion utility located at `/home/user/log_processor`.

Currently, the utility fails to build due to a circular inclusion dependency between its header files. Once you fix the build issues, you need to implement the missing core logic for parsing, checksum validation, and rate limiting.

### 1. Fix the Build Issue
The C++ project uses a simple `Makefile`. If you run `make` in `/home/user/log_processor`, it currently errors out because `parser.h` and `validator.h` mutually include each other. Refactor the headers (e.g., using forward declarations) so that the project compiles successfully using `make`. Do not change the overall architecture or remove the classes; just fix the include cycle.

### 2. Implement the Missing Logic
The tool processes a CSV log file with the following columns: `timestamp,user_id,payload_hex,checksum_hex`.
The `main.cpp` entrypoint is already written to accept two arguments: `input.csv` and `output.csv`. You must implement the processing logic in `validator.cpp` (and adjust related files as needed) to apply the following rules to each line:

**A. Checksum Validation**
The `payload_hex` is a string representing hex bytes (e.g., `4a4b4c`). The `checksum_hex` is a single hex byte (e.g., `4d`).
Compute the XOR sum of all bytes in the `payload_hex`. 
* Example: `0x4a ^ 0x4b ^ 0x4c = 0x4d`.
If the computed XOR sum does not strictly equal the provided `checksum_hex`, the request status is `INVALID_CHECKSUM`.

**B. Rate Limiting**
We allow a maximum of 3 requests per `user_id` within any 1.0-second sliding window. 
For a given request at `timestamp` (a floating point UNIX timestamp), count how many previous requests from the same `user_id` occurred in the time range `(timestamp - 1.0, timestamp]`.
If there are 3 or more previous requests in this exact window, the current request status is `RATE_LIMITED`.
*Note: Include ALL previous requests in this window for the count, regardless of whether their checksums were valid or invalid.*

**C. Output Generation**
If a request fails the checksum validation, its status is `INVALID_CHECKSUM`.
If it passes the checksum but fails the rate limit, its status is `RATE_LIMITED`.
If it passes both, its status is `OK`.

Write the results to the output CSV file appending the status as the 5th column:
`timestamp,user_id,payload_hex,checksum_hex,STATUS`

### Execution
1. Fix the code in `/home/user/log_processor`.
2. Compile the code using `make`.
3. Run the compiled executable `./processor /home/user/requests.csv /home/user/processed.csv`.

Make sure the final output strictly matches the specified format and is saved exactly at `/home/user/processed.csv`.
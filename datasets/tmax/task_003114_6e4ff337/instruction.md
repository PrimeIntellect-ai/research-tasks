You are an integration developer testing an API gateway's data transformation and rate-limiting logic. You need to write a C++ program that processes a batch of mock API requests, applies rate-limiting rules, transforms the payload encodings, and writes out a structured log.

I have provided a single-header JSON library at `/home/user/json.hpp`. 
An input file containing the mock requests is located at `/home/user/requests.json`. This file contains a JSON array of request objects. Each object has the following keys:
- `req_id` (string): Unique identifier for the request.
- `user_id` (string): Identifier of the user making the request.
- `timestamp` (integer): Epoch time in seconds. The array is already sorted chronologically.
- `payload` (string): A Base64 encoded string.

Your task is to write a C++ program (at `/home/user/api_tester.cpp`) and a `Makefile` (at `/home/user/Makefile`) to compile and run this program. 
The executable should be named `api_tester`.

The program must process the requests in order and enforce the following logic:

1. **Rate Limiting**: 
   - A maximum of 2 requests are allowed per `user_id` within any rolling 10-second window. 
   - For example, if a user makes requests at timestamps 100, 105, and 109, the first two are ACCEPTED, and the third is RATE_LIMITED. If another request comes at 111, it is ACCEPTED (the 10-second window [101, 111] only contains the request at 105).
   - Rate limiting is evaluated per user independently.

2. **Data Transformation (Encoding)**:
   - If a request is ACCEPTED, decode the Base64 `payload`.
   - Apply a bitwise XOR operation to every byte of the decoded payload using the key `0x42`.
   - Encode the resulting bytes as a continuous lowercase hexadecimal string (e.g., "0a272e").

3. **Output format**:
   - Write the results to a JSON Lines file at `/home/user/output.jsonl`.
   - Each line must be a valid JSON object with the following keys:
     - `req_id`: The ID of the request.
     - `status`: Either `"ACCEPTED"` or `"RATE_LIMITED"`.
     - `processed_payload`: The hex-encoded transformed payload (this key must *only* be present if the status is `"ACCEPTED"`).

Requirements:
- Create the C++ source file `/home/user/api_tester.cpp`.
- Create a `/home/user/Makefile` with a `default` target that compiles `api_tester.cpp` to an executable named `api_tester`. Use `g++` and compile with `-std=c++17`.
- Run your `Makefile` and execute the `./api_tester` program to generate `/home/user/output.jsonl`.
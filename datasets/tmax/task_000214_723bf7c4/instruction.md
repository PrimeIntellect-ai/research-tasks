You are an engineer tasked with porting a legacy mathematical tool into a minimal, self-contained C++ REST API that can be run inside a lightweight container. The API calculates the determinant of matrices, but it must handle custom encoding, input validation, and rate-limiting to prevent CPU exhaustion.

Your objective is to implement, compile, and run this C++ API server, and then generate a verification log.

### Step 1: Dependencies
You must write a C++ program. You may download and use single-header libraries such as `httplib.h` (yhirose) and `json.hpp` (nlohmann) to handle the REST API and JSON parsing. 
- Create your source file at `/home/user/server.cpp`.

### Step 2: API Specification
Your C++ server must listen on `0.0.0.0:8080`.
Implement a single endpoint:
`POST /api/determinant`

**Request Format:**
The endpoint accepts a JSON body:
```json
{
  "payload": "<Base64 encoded string>"
}
```

**Encoding & Validation:**
1. The `payload` must be decoded from Base64.
2. The decoded string will contain space-separated integers (e.g., `1 2 3 0 1 4 5 6 0`).
3. You must validate that there are exactly **9** integers (representing a 3x3 matrix). If the decoded string does not contain exactly 9 space-separated integers, return an HTTP `400 Bad Request` status code.

**Mathematical Operation:**
Treat the 9 integers as a 3x3 matrix (in row-major order). Calculate the determinant of this matrix. The input integers and the resulting determinant will fit safely within standard signed 32-bit integers.

**Response Format:**
On success, return an HTTP `200 OK` status with the following JSON:
```json
{
  "determinant": <integer_result>
}
```

### Step 3: Rate Limiting
Calculating matrix properties can be expensive. Implement a strict, global rate limit:
- A maximum of **2 requests** are allowed per rolling **1-second window**.
- If a 3rd request arrives within 1000 milliseconds of the 1st request in the window, the server must reject it and return an HTTP `429 Too Many Requests` status code.

### Step 4: Build and Run
- Compile your server to `/home/user/server_bin`. You may use `g++` with standard flags (e.g., `-std=c++17 -lpthread`).
- Run the server in the background.

### Step 5: Verification Log
Create a bash script at `/home/user/test_server.sh` that uses `curl` to test your server.
The script must:
1. Send a valid payload for the matrix `[2, 0, 0, 0, 2, 0, 0, 0, 2]` (Base64: `MiAwIDAgMCAyIDAgMCAwIDI=`).
2. Send an invalid payload (e.g., a 2x2 matrix).
3. Send 4 rapid requests (using the valid payload) in quick succession to trigger the rate limit.
4. Save the HTTP status codes of all these requests to `/home/user/verification.log`.

Execute your script to produce `/home/user/verification.log`. Leave your server running in the background on port 8080 when you are finished.
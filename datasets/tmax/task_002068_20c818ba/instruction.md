You are an AI assistant helping a researcher organize and serve a multimedia dataset. The researcher has an experiment video and a corresponding file of textual annotations. Your goal is to process this dataset, extract specific linear algebra features and tokens, and serve the data via two different network protocols.

Dataset inputs:
1. Video: `/app/experiment_record.mp4` (Duration: exactly 10 seconds, 30 fps).
2. Annotations: `/app/annotations.txt` (Contains exactly 10 lines of text. Line 1 corresponds to second 0, Line 2 to second 1, etc.).

Step 1: Feature Engineering & Linear Algebra Analysis
- Extract frames from the video at exactly 1 frame per second (timestamps 0.0, 1.0, 2.0, ..., 9.0).
- For each extracted frame, calculate the 3x3 sample covariance matrix of the Red, Green, and Blue color channels across all pixels. 
  - Treat the image as $N$ pixels, each being a 3D vector $[R, G, B]$ (values 0-255).
  - Compute the sample covariance matrix (divide by $N-1$).
  - Flatten the 3x3 matrix in row-major order to produce an array of 9 floats.
  - Round each float to exactly 2 decimal places.

Step 2: Tokenization
- Read `/app/annotations.txt`. 
- Tokenize each line by:
  1. Lowercasing the entire string.
  2. Removing all characters except `a-z`, `0-9`, and spaces.
  3. Splitting into a list of words using space as the delimiter.
  4. Discarding any empty strings.

Step 3: Multi-Protocol Service Implementation
You must write and run two distinct network services to expose this processed data. Both should run in the background.
Create a bash script at `/home/user/start_services.sh` that starts both services. The verifier will execute this script and wait 5 seconds before testing.

Service A (HTTP REST API):
- Listen on `127.0.0.1:8080`.
- Endpoint: `GET /data?sec=<X>` where `<X>` is an integer from 0 to 9.
- Response format: `application/json` with the following structure:
  ```json
  {
    "sec": <X>,
    "tokens": ["word1", "word2"],
    "covariance": [c00, c01, c02, c10, c11, c12, c20, c21, c22]
  }
  ```

Service B (Raw TCP Socket):
- Listen on `127.0.0.1:8081`.
- When a client connects and sends a line containing just an integer `<X>` followed by a newline (`\n`), the server should respond with the 9 flattened covariance values separated by commas, followed by a newline.
- Example request: `4\n`
- Example response: `12.34,5.67,-1.23,5.67,45.67,8.90,-1.23,8.90,10.11\n`
- The server should close the connection after sending the response.

Requirements:
- You may use any combination of languages (e.g., Python, Node.js, Bash). Python is recommended.
- Ensure the covariance calculation matches standard sample covariance (`ddof=1` in numpy).

Make sure `/home/user/start_services.sh` is executable (`chmod +x`). Once you are confident your script works and the services are ready, simply finish the task.
You are a web developer building a backend feature for a video processing platform. The new feature allows clients to query a video to find specific frames matching custom criteria expressed as logical/mathematical formulas. 

Your task is to build a gRPC service in Python that extracts frames from a video, evaluates a user-provided mathematical expression against each frame's statistics, and returns the matching frame indices. Because these expressions are provided by users, you must build a robust expression validator to prevent arbitrary code execution and resource exhaustion.

Here are the specific requirements:

**1. Protocol Definition and Build**
Create a gRPC protobuf definition at `/home/user/video_query.proto` with a service `VideoQuery` and a method `QueryFrames`.
The `QueryRequest` message should have:
- `video_path` (string)
- `expression` (string)
The `QueryResponse` message should have:
- `matching_frame_indices` (repeated int32)

Compile this proto file to Python code using `grpcio-tools`. Place the generated files in `/home/user/`.

**2. Expression Validator (Adversarial Corpus)**
Users will submit expressions like `r_mean > 120 and time_sec < 5.0` to filter frames. The allowed variables are: `frame_index` (int), `time_sec` (float), `r_mean` (float), `g_mean` (float), and `b_mean` (float).

You must write an AST-based validator in `/home/user/validator.py` containing a function:
`def is_safe_expression(expr: str) -> bool:`

This function must safely parse the expression and ensure it ONLY contains basic mathematical/logical operations (`+`, `-`, `*`, `/`, `>`, `<`, `==`, `!=`, `and`, `or`, `not`) and ONLY accesses the allowed variables or numeric constants. It must block any function calls, comprehensions, imports, or dangerous built-ins.

We have provided two corpora of expressions:
- `/app/corpus/clean/`: Contains text files with valid, safe expressions that your validator MUST accept (return True).
- `/app/corpus/evil/`: Contains text files with malicious payloads (e.g., code injection, infinite loops, memory bombs) that your validator MUST reject (return False).

**3. Video Processing gRPC Server**
Implement the gRPC server in `/home/user/server.py`. 
- The server should listen on `localhost:50051`.
- When `QueryFrames` is called, validate the `expression` using `is_safe_expression`. If it returns False, return a gRPC `INVALID_ARGUMENT` status.
- If safe, process the video specified in `video_path`. (A sample video is provided at `/app/sample_video.mp4`).
- Extract frames using `ffmpeg` or `cv2`. For each frame, calculate:
  - `frame_index`: 0-based index.
  - `time_sec`: Timestamp in seconds.
  - `r_mean`, `g_mean`, `b_mean`: The average value of the Red, Green, and Blue channels for the frame.
- Evaluate the safe expression dynamically for each frame using these variables. If the expression evaluates to True, append the `frame_index` to the response.

**4. Final Integration**
Write a client script `/home/user/client.py` that connects to the server, queries `/app/sample_video.mp4` with the expression `r_mean > g_mean + 20 and frame_index > 50`, and saves the resulting list of frame indices as a JSON array to `/home/user/result.json`.

Ensure the server is running in the background and execute your client script to generate the final `result.json`.
You are a release manager tasked with recovering a corrupted deployment configuration and standing up a local validation gateway. The configuration parameter we need was encoded into an emergency video artifact by the CI/CD pipeline before it crashed.

Your task is to extract this parameter, use it to compile a native shared library with an Assembly-level routine, and wrap it all in a Python HTTP service.

**Step 1: Video Extraction**
There is an MP4 video located at `/app/deployment_signal.mp4`. The video plays at 30 frames per second. Most of the video is black, but there is exactly one continuous sequence of pure red frames (RGB: 255, 0, 0 for all pixels).
Analyze the video to count the exact number of these pure red frames. This integer is our `DEPLOY_MAGIC_NUMBER`.

**Step 2: Polyglot Build**
You need to create a shared library named `/home/user/libdeploy.so` combining C and x86_64 Assembly.
1. Write an assembly file (`/home/user/core.asm`) that exposes a global function `get_magic_offset`. Following the Linux System V AMD64 ABI, this function should accept a single 32-bit integer argument, add the `DEPLOY_MAGIC_NUMBER` to it, and return the result.
2. Write a C file (`/home/user/wrapper.c`) that declares this external function and provides a wrapper function called `invoke_offset(int val)` which simply calls `get_magic_offset(val)` and returns the result.
3. Compile and link these into a shared library `/home/user/libdeploy.so`.

**Step 3: API Gateway**
Write and start a Python HTTP server listening exactly on `127.0.0.1:8000`. You may use the standard library or a framework like Flask/FastAPI if available.
The server must implement the following URL routes:
* `GET /status` 
  Must return a JSON response with the extracted magic number: `{"status": "ready", "magic": <DEPLOY_MAGIC_NUMBER>}`
* `GET /compute/<val>` (where `<val>` is a URL parameter parsed as an integer)
  Must load `/home/user/libdeploy.so` using `ctypes`, pass `<val>` to `invoke_offset`, and return the result as JSON: `{"result": <computed_value>}`

**Step 4: Execution**
Ensure the Python server is running in the background and listening on the specified port. Write the PID of the running server to `/home/user/server.pid`. The automated verifier will make real HTTP requests to your service to test its correctness.
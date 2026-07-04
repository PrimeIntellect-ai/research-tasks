You are a web developer building a high-performance scheduling feature for a web application. 

We have a legacy C library that acts as a Constraint Satisfaction Problem (CSP) solver for task scheduling. However, the C code is known to contain undefined behavior and memory leaks, and it uses a custom string-based serialization format. 

Your task is to fix the C library, compile it, create a Python FFI wrapper, and expose it via a local Python web service.

Here are the specific requirements:

1. **Fix the C Code (`/home/user/workspace/scheduler.c`)**:
   The C code expects an input string in the format `TaskName,Duration;TaskName,Duration;`. It assigns sequential start times.
   There are exactly three memory safety / undefined behavior bugs in the provided `scheduler.c` file:
   - An off-by-one error in memory allocation.
   - A buffer overflow vulnerability when parsing task names.
   - A memory leak.
   Identify and fix these issues so the function `char* solve_schedule(const char* input)` is safe to use. Allow task names up to 30 characters.

2. **Compile the Library**:
   Compile the fixed `scheduler.c` into a shared library named `/home/user/workspace/libscheduler.so`.

3. **Build the Python Web Service (`/home/user/workspace/app.py`)**:
   Create a Python web service (using Flask, which you should install, or the built-in `http.server`) that listens on `127.0.0.1:8080`.
   Implement an endpoint `POST /schedule` that:
   - Accepts a JSON payload like: `[{"name": "Compile", "duration": 5}, {"name": "Test", "duration": 2}]`
   - **Serializes** this JSON into the custom string format expected by the C library (`Compile,5;Test,2;`).
   - Calls the `solve_schedule` C function via **FFI (ctypes)**. Ensure you correctly set `argtypes` and `restype` and handle the returned memory appropriately (the C function returns a malloced string which needs to be freed, you'll need to expose `free` from libc to clean it up in Python).
   - **Deserializes** the custom string returned by the C function (format `Compile:0;Test:5;`) back into a JSON array of objects: `[{"name": "Compile", "start": 0}, {"name": "Test", "start": 5}]`.
   - Returns the JSON payload with a 200 OK status.

4. **Verify the Service**:
   Start your web service in the background. Then, write and execute a script that sends the following JSON payload to `http://127.0.0.1:8080/schedule`:
   ```json
   [
     {"name": "DesignSystemArchitecture", "duration": 15},
     {"name": "ImplementFFI", "duration": 8},
     {"name": "WriteTests", "duration": 4}
   ]
   ```
   Save the exact JSON response returned by the server to `/home/user/workspace/final_schedule.json`.

Ensure your service is running and `final_schedule.json` is correctly populated before you finish.
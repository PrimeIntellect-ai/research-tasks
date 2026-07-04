You are a platform engineer tasked with fixing a broken CI/CD pipeline for a legacy polyglot microservice called `task-broker`. The service pairs a highly optimized C++ core data structure with a Go-based REST API that utilizes CGO for polyglot interoperability.

Currently, the service fails to build and fails its concurrency tests. 

Here is what you need to do to fix the pipeline:

1. **Resolve Circular Dependency**: The C++ code located in `/home/user/app/cpp/` fails to compile because `Task.h` and `Worker.h` have a circular include dependency. Refactor the headers using forward declarations to break the cycle so the code compiles.
2. **Implement Missing Core Logic**: The custom data structure in `/home/user/app/cpp/TaskQueue.cpp` is missing the implementation for the `Task* pop_task()` method. You must implement it. It must extract and return the task with the highest priority (highest integer value) from the `std::vector<Task*> tasks` member. It must be thread-safe (use the existing `std::mutex mtx` member) because the Go REST API calls it concurrently from multiple goroutines. If the queue is empty, return `nullptr`.
3. **Polyglot Build Script**: Write a shell script at `/home/user/build.sh` that:
   - Compiles the C++ code into a shared library `libtaskqueue.so` (ensure you use `-fPIC` and `-shared`). Place the library in `/home/user/app/lib/`.
   - Builds the Go service located in `/home/user/app/go/`. The Go build must dynamically link to `libtaskqueue.so`. Output the Go binary to `/home/user/app/task-broker`.
   - Ensure the script has executable permissions.
4. **Integration Testing**: 
   - Start the compiled `task-broker` binary in the background (it listens on port 8080). Make sure the `LD_LIBRARY_PATH` is set correctly so the Go binary can find the shared library.
   - Write a Python script at `/home/user/test_system.py` that interacts with the REST API.
   - The script should send three concurrent POST requests to `http://localhost:8080/enqueue` with JSON payloads: `{"id": "task1", "priority": 10}`, `{"id": "task2", "priority": 30}`, and `{"id": "task3", "priority": 20}`.
   - After ensuring all tasks are enqueued, send three sequential GET requests to `http://localhost:8080/dequeue`.
   - Parse the JSON responses (e.g., `{"id": "task2"}`) and write the IDs of the dequeued tasks, each on a new line, to `/home/user/api_output.txt`.

The automated test will verify that your build script successfully produces the binaries and that `/home/user/api_output.txt` contains the correct task IDs in the expected priority order.
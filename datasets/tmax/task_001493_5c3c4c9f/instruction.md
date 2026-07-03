You are acting as a release manager preparing the deployment systems for our new infrastructure rollout. As part of this, we have a microservice that calculates deployment schedules using a constraint satisfaction algorithm written in C, wrapped by a Rust REST API. 

However, the build is currently broken and the API is incomplete. 

Here is what you need to do:

1. **Fix the Vendored C Library**
   We vendor a third-party C library at `/home/user/app/vendor/libcsched`. 
   - The Makefile is currently failing to build a shared library (`libcsched.so`) because it is missing the necessary position-independent code flags and shared object flags. Fix the Makefile.
   - The library has a memory safety bug (undefined behavior) in the `calculate_schedule` function inside `schedule.c`. It frequently segfaults due to an out-of-bounds array write. Identify and fix this memory bug.
   - Build the shared library.

2. **Complete the Rust REST API**
   The Rust wrapper is located at `/home/user/app/scheduler-api`.
   - Implement the FFI bindings to call the C function: `int calculate_schedule(const int* task_durations, int num_tasks, int* output_schedule);`.
   - Create a REST endpoint `POST /schedule` that accepts JSON: `{"tasks": [list of integers]}`.
   - The endpoint must pass these tasks to the C library, read the generated schedule, and return it as JSON: `{"schedule": [list of integers]}`.
   - You must implement an authentication middleware or check in the endpoint: it MUST require an `Authorization` header with the exact value `Bearer RM-DEPLOY-999`. Unauthenticated requests must receive a `401 Unauthorized` response.

3. **Run the Service**
   - Start the Rust service. It MUST listen on exactly `127.0.0.1:8080`.
   - Leave the server running in the background so it can be evaluated. Create a file `/home/user/app/server.pid` containing the PID of your running Rust server so the verifier knows it is ready.

Ensure your Rust code compiles cleanly and correctly links against the fixed C library. You may need to set `LD_LIBRARY_PATH` when running the Rust binary so it can find `libcsched.so`.
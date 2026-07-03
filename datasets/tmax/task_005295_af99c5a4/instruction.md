You are a systems programmer and backend developer tasked with resolving a complex system involving C, Rust, and Python.

In `/home/user/workspace`, you have a multi-tier application:
1. `c_lib/`: A C library (`libdataproc.so`) that allocates and processes strings.
2. `rust_lib/`: A Rust FFI layer (`librustffi.so`) that wraps the C library.
3. `python_api/`: A Python FastAPI application (`app.py`) that uses `ctypes` to call the Rust FFI layer and exposes a REST API.

Currently, the system is completely broken:
1. **Rust Borrow Checker Error:** The Rust library fails to compile due to a borrow checker/lifetime issue in `src/lib.rs` involving CString and FFI.
2. **Linking Issue:** Once compiled, the Python API fails to start because it cannot resolve the shared C library dependencies dynamically.
3. **Memory Leak:** The FFI layer leaks memory every time the text processing function is called because it fails to properly free the memory allocated by the C library.
4. **Missing API Endpoints:** The FastAPI application is missing a `/stats` endpoint.

Your objectives:
1. **Fix the Rust Code:** Edit `/home/user/workspace/rust_lib/src/lib.rs` so that it successfully compiles without borrow checker errors.
2. **Fix the Memory Leak:** Modify the Rust FFI wrapper to ensure the memory allocated by the C library's `process_text` function is properly freed using the C library's `free_text` function.
3. **Fix the Linking Issue:** Make any necessary configuration or code changes so that running `python3 app.py` in `/home/user/workspace/python_api/` successfully loads both `librustffi.so` and `libdataproc.so`.
4. **Update the Python API:** Add a `GET /stats` endpoint to `/home/user/workspace/python_api/app.py` that returns the exact JSON response: `{"status": "ok", "processed_count": <integer>}`. The `processed_count` should track how many times the `/process` endpoint has been called since the server started.
5. **Create a Report:** Create a file at `/home/user/workspace/resolution.json` with the following schema:
```json
{
  "rust_compile_fix": "<brief description of how you fixed the borrow checker>",
  "memory_leak_fix": "<brief description of how you fixed the memory leak>",
  "linking_fix": "<brief description of how you fixed the linking issue>"
}
```

Constraints:
- Do not modify the C code in `c_lib/`. You must compile it using the provided Makefile.
- Do not change the function signatures exported by the Rust library.
- Use Python 3.10+ and standard FastAPI/Uvicorn practices.
You are an open-source maintainer reviewing a pull request for a project that uses Python for structured data parsing and a Rust extension for high-performance string manipulation. The PR author has abandoned the PR, which is currently broken and failing the CI pipeline.

The repository is located at `/home/user/data_parser/`.

The PR introduced several issues that you need to fix:
1. **Rust Borrow Checker & ABI Issues:** The Rust library (`/home/user/data_parser/src/lib.rs`) fails to compile. The PR author tried to return a C-string to Python but created a dangling pointer (borrow checker / lifetime issue). You need to fix it so it properly returns an owned string across the C-ABI boundary.
2. **Memory Leak:** The Python wrapper (`/home/user/data_parser/parser.py`) loads the returned string via `ctypes`. However, even if the Rust code is fixed to return a valid pointer, it will leak memory because the pointer is never freed. You must implement an appropriate `free_string` function in the Rust code and call it from the Python code after parsing the data.
3. **Structured Data Parsing:** The Rust code returns a JSON string. The Python script currently fails to parse it correctly. Fix `parser.py` so it parses the JSON, extracts the value of `["payload"]["id"]`, and writes exactly that integer value into `/home/user/data_parser/output.json`.
4. **CI/CD Setup:** The CI script `/home/user/data_parser/ci.sh` is missing the correct `rustc` command to compile the Rust file into a shared library (`librust_parser.so`) and doesn't run the Python script. Fix the CI script so it compiles the library, runs `parser.py`, and exits with code 0.

Your task is complete when:
- `bash /home/user/data_parser/ci.sh` runs successfully.
- The memory leak is properly handled (Rust provides a free function, Python calls it).
- `/home/user/data_parser/output.json` contains the correct parsed integer.
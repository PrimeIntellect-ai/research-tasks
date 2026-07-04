You are tasked with fixing a Rust project that is failing to compile, configuring it to build a shared library, and writing a Python script to benchmark its exported functions. 

You have a workspace located at `/home/user/rust_ffi_project/sorter`. It is a Rust library designed to expose two sorting algorithms (Merge Sort and Quick Sort) via a C ABI so they can be called from Python.

However, the project currently fails to compile properly as a C-compatible shared library due to missing ABI directives, incorrect configuration, and standard Rust compilation errors.

Your objectives are:
1. **Fix the Rust library**: 
   - Modify `/home/user/rust_ffi_project/sorter/Cargo.toml` to ensure the crate compiles as a C dynamic library (`cdylib`).
   - Fix `/home/user/rust_ffi_project/sorter/src/lib.rs` so that the functions `merge_sort_ffi` and `quick_sort_ffi` are correctly exported with the C ABI and without mangled names. Fix any syntax errors preventing compilation.
   - Build the shared library (`cargo build --release`).

2. **Write a Python Benchmarking Script**:
   - Create a script at `/home/user/rust_ffi_project/benchmark.py`.
   - Use `ctypes` to load the compiled shared library (which will be located at `/home/user/rust_ffi_project/sorter/target/release/libsorter.so`).
   - Define the correct `argtypes` and `restype` for the two C functions. The C signature equivalent is `void function_name(int32_t* data, size_t len)`.
   - Seed Python's `random` module with `42` and generate an array of 50,000 random integers between `0` and `1000000`.
   - Make two copies of this array. Pass one to the Rust merge sort and the other to the Rust quick sort.
   - **Verification (Sorting & Diffing)**: Ensure both Rust algorithms produced the exact same sorted array. If they match completely, write the word `MATCH` to `/home/user/rust_ffi_project/verification.txt`. If they do not match, write the differences (any format) to the file.
   - **Benchmarking**: Run a benchmark where you sort a fresh shuffled copy of the 50,000-element array 5 times for each algorithm. Measure the time taken using `time.perf_counter()`.
   - Write a report to `/home/user/rust_ffi_project/report.txt` containing the average time taken for each, formatted exactly as follows:
     ```
     Algorithm: Merge Sort, Avg Time: <X.XXXX> seconds
     Algorithm: Quick Sort, Avg Time: <Y.XXXX> seconds
     ```
     (Where `<X.XXXX>` and `<Y.XXXX>` are the times rounded to 4 decimal places).

Ensure your Python script runs without errors and produces the two required output files (`verification.txt` and `report.txt`).
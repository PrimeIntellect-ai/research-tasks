You are a Machine Learning Engineer responsible for preparing and validating a large-scale training dataset. Raw model outputs and sensor data have been dumped as JSON files. Before we ingest these into our large-scale data storage (HDF5), we need an ultra-fast validation tool written in C++.

We are using the `simdjson` library for fast JSON parsing. The source code for `simdjson` v3.6.0 is vendored at `/app/simdjson-3.6.0`.

Your task consists of three parts:

1. **Numerical Library Configuration (Fixing the Package)**
   The vendored `simdjson` package is currently failing to build due to a configuration error introduced in its build system (CMakeLists.txt). 
   - Identify and fix the perturbation in `/app/simdjson-3.6.0/CMakeLists.txt`.
   - Build and install the library locally to `/home/user/local`.

2. **Implementation (Model Output Validation)**
   Write a C++ program at `/home/user/src/validator.cpp`. This program must link against your installed `simdjson` library.
   The program must accept exactly one argument: the absolute path to a JSON file.
   It must parse the JSON file and validate it against the following strict model output rules:
   - The JSON object must contain a key `"status"` with the exact string value `"success"`.
   - The JSON object must contain a key `"data"`, which must be a 1D array of exactly 256 floating-point numbers.
   - None of the numbers in `"data"` can be `NaN` or `Infinity`.
   - All numbers in `"data"` must be strictly between `-10.0` and `10.0` (inclusive).
   
   If the file is valid and meets all conditions, your program must print EXACTLY the string `ACCEPT` to standard output and exit with code 0.
   If the file violates ANY of the conditions (or is malformed JSON), your program must print EXACTLY the string `REJECT` to standard output and exit with code 0.

3. **Compilation**
   Compile your program into an executable located at `/home/user/src/validator`. Ensure it correctly statically or dynamically links to the `simdjson` library you installed in `/home/user/local`.

Note: You can test your program against sample data if you wish, but the automated test suite will run your `/home/user/src/validator` binary against a holdout dataset of clean and corrupted JSON files to ensure perfect accuracy.
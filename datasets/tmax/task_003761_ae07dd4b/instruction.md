You are a mobile build engineer tasked with setting up a cross-language testing pipeline for a core Rust library that behaves differently across target platforms. We are simulating cross-compilation by using Cargo features and testing the FFI boundaries using Python.

Your objective is to create the library, set up conditional builds, and write an integration test pipeline.

Perform the following steps exactly as specified:

1. **Rust Library Setup:**
   - Create a new Rust project named `mobile_sensor` in `/home/user/mobile_sensor`.
   - Configure `Cargo.toml` so the crate compiles to a C-dynamic library (`cdylib`).
   - Define two Cargo features: `android` and `ios`.
   - Add the `libc` crate as a dependency (use standard dependency management).

2. **FFI Implementation:**
   - In `src/lib.rs`, implement a C-callable function with the following signature (conceptually in C):
     `int32_t process_sensor_data(const float* data, size_t len)`
   - The function must iterate over the provided float array and calculate the sum.
   - Use conditional compilation (`#[cfg(feature = "...")]`) to alter the return value:
     - If the `android` feature is enabled, multiply the sum by `2.0`, truncate to an integer (`i32`), and return it.
     - If the `ios` feature is enabled, multiply the sum by `3.0`, truncate to an integer (`i32`), and return it.
     - If neither feature is enabled, return `-1` (as an `i32`).
   - Ensure the function is safely exported (`#[no_mangle]`, `pub extern "C"`). Handle null pointer inputs gracefully by returning `-1`.

3. **Python Test Script:**
   - Write a Python script at `/home/user/verify.py` that uses the `ctypes` module to load a shared library path provided as the first command-line argument (`sys.argv[1]`).
   - Set up the proper `argtypes` and `restype` for the `process_sensor_data` function.
   - The script must call the FFI function with an array of exactly 3 floats: `[1.5, 2.5, 3.5]`.
   - The script must print *only* the returned integer to standard output.

4. **Build and Test Pipeline:**
   - Create a bash script at `/home/user/run_all_tests.sh`.
   - The script must:
     a. Create a directory `/home/user/libs/`.
     b. Build the `mobile_sensor` crate in release mode three times: without features, with the `android` feature, and with the `ios` feature.
     c. After each build, rename and copy the resulting `.so` file to `/home/user/libs/libmobile_sensor_default.so`, `/home/user/libs/libmobile_sensor_android.so`, and `/home/user/libs/libmobile_sensor_ios.so` respectively. (Note: Cargo will overwrite the default output file if you don't copy it between builds).
     d. Execute `/home/user/verify.py` for each of the three libraries.
     e. Save the output of the Python script into a file `/home/user/final_output.log` formatted exactly like this:
        ```
        default: <output>
        android: <output>
        ios: <output>
        ```
   - Make the bash script executable and run it to produce `/home/user/final_output.log`.
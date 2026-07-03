You are the release manager for a numerical computing project. The team is preparing for a new deployment, but the build pipeline is currently broken due to issues across our multi-language stack (Python, C, and Rust). You need to fix the codebase, implement a missing mathematical algorithm in Python, and write a shell script to orchestrate the build and testing.

The project is located in `/home/user/release_prep/` (you should create this directory and the files below if they don't exist, though typically assume you are starting from scratch).

Here are the requirements:

**1. The C Extension (Memory Safety Fix)**
Create `/home/user/release_prep/c_src/math_core.c` with the following initial code:
```c
#include <stdlib.h>
#include <stdio.h>

// Calculates the cumulative sum of an array.
// BUG: There is an off-by-one buffer overflow here causing Undefined Behavior.
void cumsum(double* input, double* output, int n) {
    double current_sum = 0.0;
    for (int i = 0; i <= n; i++) {
        current_sum += input[i];
        output[i] = current_sum;
    }
}
```
*Task:* Fix the undefined behavior / memory safety issue in the `cumsum` function.

**2. The Rust Validator (Borrow Checker Fix)**
Create `/home/user/release_prep/rust_src/validator.rs` with the following initial code:
```rust
fn calculate_hash(data: String) -> usize {
    data.len() * 42
}

fn main() {
    let report = String::from("Release Candidate 1");
    let hash_val = calculate_hash(report);
    // BUG: borrow checker error here because `report` was moved.
    println!("Report: {} has hash: {}", report, hash_val);
}
```
*Task:* Fix the Rust code so it compiles without ownership/borrow checker errors. Do not change the output format of the `println!`.

**3. The Python Core (Numerical Algorithm)**
Create `/home/user/release_prep/python_src/algo.py`. 
*Task:* Implement a Python script that:
a) Implements Simpson's 1/3 rule for numerical integration to approximate the integral of `f(x) = x^3 - 2x^2 + 5` from `x = 0` to `x = 2` using exactly `n = 100` subintervals.
b) Calls the compiled C extension (`libmath.so`) to calculate the cumulative sum of the array `[1.0, 2.0, 3.0, 4.0, 5.0]`. Use `ctypes` to load the C library.
c) Prints the exact following format to stdout:
`Integral: <value>` (rounded to 4 decimal places)
`Cumsum: <last_value_of_cumsum_array>` (rounded to 1 decimal place)

**4. The Release Script (Cross-compilation & Builds)**
Create a bash script at `/home/user/release_prep/build_release.sh`.
*Task:* This script must:
a) Compile `c_src/math_core.c` into a shared library `c_src/libmath.so` using `gcc`. Include the conditional build flag `-DRELEASE_MODE=1` (even if unused in the current C code, it's required for our build system compliance).
b) Compile `rust_src/validator.rs` into an executable `rust_src/validator` using `rustc`.
c) Run the Rust executable and append its output to `/home/user/release_prep/release_report.txt`.
d) Run the Python script `python_src/algo.py` and append its output to `/home/user/release_prep/release_report.txt`.

Once you have written and fixed all the files, execute `bash /home/user/release_prep/build_release.sh` so that `/home/user/release_prep/release_report.txt` is populated correctly.
You are a Site Reliability Engineer tasked with creating a lightweight storage monitoring health check for a local CI pipeline. The system needs to ensure that a specific application data directory does not exceed its allocated quota before the CI pipeline proceeds.

Your task is to implement this health check using Rust and integrate it into a bash-based CI step. 

Follow these exact requirements:

1. **Rust Health Check (`/home/user/monitor.rs`)**:
   - Write a Rust program that calculates the total size (in bytes) of all files directly inside `/home/user/app_data` (you only need to check the flat directory, no subdirectories).
   - If the total size is strictly greater than `5000` bytes, the program should exit with status code `1` (indicating a quota breach).
   - If the total size is `5000` bytes or less, the program should exit with status code `0`.
   - The Rust program should not produce any standard output.

2. **CI Pipeline Script (`/home/user/ci_step.sh`)**:
   - Write a bash script that acts as our CI test runner.
   - The script must first compile the Rust program using `rustc monitor.rs`.
   - Next, it must execute the compiled `./monitor` binary.
   - You must configure the environment so that dates are generated in the `Asia/Tokyo` timezone.
   - Based on the exit code of `./monitor`, the script must append exactly one line to `/home/user/build.log`.
   - If the exit code is `0`, append: `Status: PASS - YYYY-MM-DD HH:MM:SS`
   - If the exit code is `1`, append: `Status: FAIL - YYYY-MM-DD HH:MM:SS`
   - (Replace `YYYY-MM-DD HH:MM:SS` with the exact current time in the `Asia/Tokyo` timezone).

**Execution**:
Once you have written both files, make `/home/user/ci_step.sh` executable and run it once to generate the `/home/user/build.log` file. The directory `/home/user/app_data` will already exist and contain files for you to test against.
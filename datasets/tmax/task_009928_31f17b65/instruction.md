Wake up! It's 3 AM and our high-frequency trading weight calculation service is failing. 

The service is located at `/home/user/weight_service`. It's a Rust application that processes incoming price ticks concurrently. We are seeing intermittent alerts where the service outputs `inf` (Infinity) or `NaN` during high-traffic bursts, causing severe downstream numerical instability.

Here is what we know:
1. The Rust service delegates the core math to a legacy pre-compiled C library (`/home/user/weight_service/libcalc.so`). We lost the source code for this library years ago.
2. The crash only happens under heavy concurrent load. We suspect there is a thread-safety issue (like a race condition on a shared state) inside the black-box C library itself.

Your mission:
1. **Reverse Engineer:** Analyze `/home/user/weight_service/libcalc.so` to determine the exact mathematical formula it applies in the `compute_weights(double x, double y)` function.
2. **Rewrite:** Remove the C dependency entirely. Replace the FFI call in the Rust service with a pure, safe Rust implementation of the reversed mathematical formula.
3. **Fix the Race Condition:** Ensure your new pure Rust implementation does not share mutable state across threads, eliminating the data race and the resulting numerical instability.
4. **Build & Verify:** Ensure the service in `/home/user/weight_service` compiles successfully with `cargo build --release`. 

Finally, create a file named `/home/user/resolution.txt` containing exactly two lines:
Line 1: The mathematical formula you reverse-engineered, written as a valid Rust expression using variables `x` and `y` (e.g., `(x * y) + 2.0`).
Line 2: The output of your pure Rust `compute_weights(10.0, 5.0)`.

Good luck. The market opens in a few hours.
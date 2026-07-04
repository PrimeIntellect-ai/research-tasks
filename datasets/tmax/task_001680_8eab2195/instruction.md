You are an operations engineer triaging a critical incident for the data science team. They have a Rust-based data processing service located at `/home/user/incident-1042` that calculates the numerical derivative of a time-series metric array using the central difference method. 

However, the application crashes with a panic when processing production data, causing pipeline failures. The source code is in `/home/user/incident-1042/src/main.rs`.

The central difference method is defined as:
`d[i] = (data[i+1] - data[i-1]) / 2.0`

For the boundaries (which the original developer clearly didn't implement correctly, leading to off-by-one and out-of-bounds errors), you must use:
- Forward difference for the first element: `d[0] = data[1] - data[0]`
- Backward difference for the last element: `d[n-1] = data[n-1] - data[n-2]`
If the data length is 1, the derivative should just be `[0.0]`. If it is 0, return an empty vector.

Your tasks are to:
1. Debug the panic using standard tools or an interactive debugger (the application will currently crash if you run `cargo run`).
2. Fix the boundary conditions and off-by-one errors in the `compute_derivative` function in `src/main.rs`.
3. Construct a regression test. You must add a test module in `src/main.rs` that includes a test function exactly named `test_boundary_conditions`. This test should verify that passing an array of `[1.0, 4.0, 9.0, 16.0]` returns `[3.0, 4.0, 6.0, 7.0]`.
4. Ensure `cargo test` passes.
5. Run the corrected application, which will process the production data in `/home/user/incident-1042/data.csv`. The application prints a single floating-point number representing the sum of the derivatives.
6. Write this final sum to a file exactly at `/home/user/resolution.txt`.

Do not change the application's CLI argument logic; it is already configured to read `data.csv` from the current working directory if no arguments are provided.
You are tasked with fixing a broken Rust project located at `/home/user/math_ws_server`. This project is intended to be a WebSocket server that receives JSON requests containing an integer `R`, and responds with a sorted JSON array of all non-negative integer pairs `[x, y]` that satisfy the Diophantine equation $x^2 + y^2 = R$.

Currently, the project fails to compile due to several issues:
1. Borrow checker and type errors in `src/math.rs` where the merging and sorting of results is supposed to happen.
2. Unfinished WebSocket message handling in `src/server.rs`.
3. An unimplemented constraint satisfaction numerical algorithm: `solve_diophantine(r: i32) -> Vec<(i32, i32)>` in `src/math.rs`.

Your tasks are:
1. **Fix the compilation errors** in the Rust project.
2. **Implement the numerical algorithm** in `solve_diophantine` to find all pairs of non-negative integers `(x, y)` such that $x^2 + y^2 = R$.
3. **Ensure the output is sorted** first by `x` in ascending order, then by `y` in ascending order.
4. **Complete the WebSocket server logic** so it runs on `127.0.0.1:8080` at the `/solve` route. It must accept a JSON string like `{"r": 65}` and return a JSON array of arrays, e.g., `[[1, 8], [4, 7], [7, 4], [8, 1]]`. If a message is invalid, ignore it.
5. **Start the server** in the background.
6. **Test the server** by writing an auxiliary script in any language of your choice. Send the following values of `R` to the server: `25`, `65`, and `1105`. Write the raw server responses (just the JSON arrays, one per line) to a log file at `/home/user/ws_output.log`.

The final state must have the compiled Rust server running on port 8080, and the `/home/user/ws_output.log` file strictly containing the three JSON arrays corresponding to the inputs `25`, `65`, and `1105`.
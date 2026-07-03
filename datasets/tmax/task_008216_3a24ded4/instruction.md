You are an Operations Engineer triaging a critical incident. Our internal math service, which calculates the roots of $f(x) = x^3 - x$ using the Newton-Raphson method, has been crashing and hanging in production.

We have captured the recent network traffic in `/home/user/traffic.pcap`. The service receives initial guesses as plain text UDP payloads on port `8080`.

Here is your task:
1. Extract all the initial guesses (payloads) sent to UDP port 8080 from `/home/user/traffic.pcap`. Each packet contains a single floating-point number as text.
2. Review the source code for the service at `/home/user/newton_solver.cpp`. It contains two critical bugs that cause the production crashes:
   - An off-by-one boundary condition that causes memory corruption.
   - A convergence failure bug where specific inputs cause a division by zero (or near zero) leading to NaN values, hanging, or undefined behavior.
3. Fix the bugs in `newton_solver.cpp`. Your fix must ensure that:
   - Memory boundaries are strictly respected (no writing out of bounds).
   - If the derivative $f'(x)$ is extremely close to 0 (absolute value `< 1e-6`), the solver must gracefully abort instead of dividing by zero.
   - The loop correctly terminates without crashing.
4. Compile your fixed C++ program.
5. Run the compiled program against every initial guess extracted from the pcap file, in the order they appear in the capture.
6. Write the output of each run to `/home/user/results.log`. The output format for each line in the log must be exactly:
   `GUESS: <extracted_guess> RESULT: <output_from_program>`

Example of expected lines in `results.log`:
`GUESS: 2.5 RESULT: CONVERGED: 1`
`GUESS: 0.57735 RESULT: FAILED`

All necessary tools (like `tshark`, `tcpdump`, `g++`) are available in your environment.
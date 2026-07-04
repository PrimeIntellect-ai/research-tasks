**IT Support Ticket #4022: Physics Engine Numerical Instability**

**Description:**
Hello Support,

Our internal physics engine, written in Rust, is producing wildly incorrect results (often evaluating to exactly zero or large erroneous values) for very small input values. 

Here is what we know:
1. The engine evaluates a specific formula. I've attached a screenshot of the mathematical formula from our textbook at `/app/formula.png`.
2. The engine crashed recently on a specific input value. The logger was down, but I dumped the raw memory segment near the panic into `/home/user/crash.bin`. The exact input value `x` (which is an IEEE-754 64-bit float, little-endian) is stored in this binary file immediately following the ASCII string marker `FAIL_X_VAL=`.
3. The codebase is located at `/home/user/engine`. 

**Your Task:**
1. Analyze `/home/user/crash.bin` to extract the exact `x` value that caused the failure.
2. Review the formula in `/app/formula.png` and fix the Rust implementation in `/home/user/engine/src/main.rs` to compute this formula without suffering from catastrophic cancellation or numerical instability when `x` is very small.
3. Recompile the engine.
4. Run the fixed engine, passing the extracted `x` value as the sole command-line argument.
5. Save the standard output (just the final floating-point result) to `/home/user/result.txt`.

Please ensure your numerical implementation is highly accurate (error < 1e-7).
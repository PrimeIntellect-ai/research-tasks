You are a backend web developer working on a high-performance Node.js service. The service requires an extremely fast Greatest Common Divisor (GCD) calculation for some cryptographic features, so the team decided to implement it in C++ and call it from Node.js using Foreign Function Interface (FFI).

However, the current workspace at `/home/user/math-addon` is broken. The previous developer left it in a non-working state. 

Your goals are to resolve all the issues, compile the library, and pass the property-based tests:

1. **Fix Dependencies:** The `package.json` has an invalid/conflicting dependency configuration preventing `npm install` from succeeding. Fix the `package.json` (you may update or align versions, removing conflicting constraints, keeping `ffi-napi` and `fast-check` intact) and successfully install the node modules.
2. **Repair Makefile:** The C++ library is located in `/home/user/math-addon/src`. The `Makefile` is broken and fails to produce a valid shared library that FFI can load. Fix the `Makefile` to correctly build a shared library named `libmath.so` in the `src` directory.
3. **Debug C++ Code:** The C++ implementation in `src/math.cpp` contains a logical flaw. When it runs, the property-based tests fail (or crash). Identify the bug in the `fast_gcd` function and fix it so it accurately computes the GCD for any two unsigned 64-bit integers.
4. **Run Tests:** Once the C++ code is fixed and compiled, run `npm test`.
5. **Record Verification:** When the tests pass, run `npm test > /home/user/success.txt 2>&1` so the system can verify your completion.

All files are located within `/home/user/math-addon`. You have all the standard compiler tools (`g++`, `make`) and Node.js/npm installed.
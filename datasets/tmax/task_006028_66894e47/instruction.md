You are a DevOps engineer debugging a mathematical backend service. Recently, the service has started producing erroneous negative results in production, triggering alerts.

There are two separate issues you must resolve:
1. **Integer Overflow Regression**: The service code in the Git repository (`/home/user/repo`) recently suffered a regression causing integer overflow for large inputs.
2. **Missing Bitwise Logic**: The repository implementation has never fully matched the behavior of the original proprietary binary (`/home/user/legacy/oracle`). The oracle applies a final bitwise XOR operation with a specific 32-bit hex constant that is missing from the open-source C code.

Your objectives:
1. **Log Analysis**: Inspect the logs in `/home/user/system_logs/` (`api_gateway.log` and `calc_service.log`). Correlate the logs to find the first request ID that failed (i.e., produced a negative result) and extract its `x` and `y` input values.
2. **Git Bisection**: Use `git bisect` in `/home/user/repo` to find the exact commit hash that introduced the integer overflow regression.
3. **Reverse Engineering**: Analyze the stripped binary `/home/user/legacy/oracle` to discover the missing 32-bit hex constant used in its XOR operation.
4. **Code Fix**: Modify `/home/user/repo/calc.c` on the `master` branch to fix the integer overflow, AND apply the missing XOR operation using the constant you reverse engineered. Compile it to ensure it works.
5. **Reporting**: Create a final report at `/home/user/resolution.txt` with the exact format below.

**Format for `/home/user/resolution.txt`:**
```
First failing REQ: <REQUEST_ID>
Failing inputs: x=<X_VAL> y=<Y_VAL>
Overflow commit: <FULL_COMMIT_HASH>
Oracle XOR constant: 0x<HEX_CONSTANT_UPPERCASE>
Fixed program output for failing inputs: <FINAL_CORRECT_OUTPUT>
```

Example of correct formatting:
```
First failing REQ: REQ-9999
Failing inputs: x=10 y=20
Overflow commit: 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b
Oracle XOR constant: 0xDEADBEEF
Fixed program output for failing inputs: 123456789
```

*Note: You may use any tools available in the environment (`gcc`, `gdb`, `objdump`, `git`, standard Unix text processing utilities).*
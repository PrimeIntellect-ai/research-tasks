You are an IT support technician handling an escalated ticket from the Quantitative Research team.

**Ticket #8841: Physics simulation wrapper failing**
*User Statement:*
"I'm trying to run my python simulation script `simulate.py` which depends on a C-extension wrapper for our proprietary pre-compiled library `libcore.so`. 
First, my build script `build.sh` is failing with a linker error. I suspect the function name in my `wrapper.c` might not match the exported symbol in `libcore.so`, but I've lost the original C header file and can't check the source.
Second, even if I get it to compile, the researcher mentioned that the fallback function in my Python script (`fallback_decay`) suffers from severe numerical instability (catastrophic cancellation) for very small inputs like `x = 1e-8`, returning `0.0` instead of the mathematically correct limit.

Can you:
1. Figure out the correct exported function name from `libcore.so` and fix `wrapper.c` so that `./build.sh` succeeds.
2. Fix the numerical instability in the `fallback_decay(x)` function inside `simulate.py` so it computes the correct physical value for infinitesimally small inputs (the mathematical formula is $f(x) = \frac{1 - \cos(x)}{x^2}$).
3. Run `simulate.py` so it outputs the correct value into `/home/user/ticket_8841/result.txt`."

**Environment Details:**
- All files are located in `/home/user/ticket_8841/`
- Run your fixed code to ensure `/home/user/ticket_8841/result.txt` is generated successfully. Ensure the output is accurate to at least 5 decimal places.
You are a machine learning engineer preparing observational data for a probabilistic model. As part of the data ingestion pipeline, you need to compute the cumulative density of certain normalized variables using a custom numerical integration library. 

The integration library is vendored in the environment at `/app/libsim_model-1.2.0`. 
However, you have noticed two critical issues with it:
1. The library currently fails to compile. The `Makefile` attempts to build a shared library `libsim_model.so` but forgets to link the standard math library, causing undefined symbol errors for mathematical functions (like `exp` and `fabs`).
2. Even if compiled, the numerical integrator diverges on some inputs. Upon inspection, the adaptive step-size logic in `integrator.c` has a glaring error: the new time-step `dt` is incorrectly scaled proportional to the integration `error` (e.g., `dt = dt * (error / tolerance);`). This causes the step size to explode when the error is high. It should be inversely proportional (i.e., scaling by `(tolerance / error)`).

Your task:
1. Fix the `Makefile` in `/app/libsim_model-1.2.0` so that it builds `libsim_model.so` correctly.
2. Fix the step-size adaptation bug in `/app/libsim_model-1.2.0/integrator.c`.
3. Compile the vendored library.
4. Write a C program at `/home/user/prepare_data.c` that compiles to an executable at `/home/user/prepare_data`.
5. Your executable must link against the fixed `libsim_model.so`. It should accept exactly one command-line argument: a floating-point value `x`.
6. The executable must parse the argument `x`, call the library function `double integrate_density(double x);`, and print the returned value to standard output formatted to exactly 6 decimal places (e.g., `printf("%.6f\n", result);`).

Make sure your executable handles the library correctly (you may need to set `LD_LIBRARY_PATH` or use rpath so your executable can find the shared library at runtime). Our automated verification will invoke `/home/user/prepare_data` with hundreds of different inputs and check the outputs against a golden standard.
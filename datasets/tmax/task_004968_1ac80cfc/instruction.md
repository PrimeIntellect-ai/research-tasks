You are a mobile build engineer maintaining a cross-platform pipeline. We are integrating a high-performance C mathematical module into our Python build tooling, but the integration is currently broken.

You have been given a workspace at `/home/user/math_module/` and a specification image at `/app/spec.png`.

Your objectives are:
1. **Analyze Specifications:** Read the image at `/app/spec.png` (you can use `tesseract`). It contains a mathematical formula (a polynomial) and a semantic version requirement for the build environment.
2. **Environment & Patching:** Check the version inside `/home/user/math_module/version.txt`. If and only if it is strictly greater than or equal to the required semantic version from the image, apply the patch `/home/user/math_module/fast_math.patch` to `mathops.c`. 
3. **C Code Update:** Update the C function `compute_poly` in `mathops.c` to compute the exact polynomial specified in the image.
4. **Fix the Build:** The `Makefile` in `/home/user/math_module/` is broken. Fix it so that running `make` successfully compiles `mathops.c` into a shared library named `libmathops.so` (ensure proper ABI and Position Independent Code flags).
5. **Python FFI:** Write a Python script at `/home/user/math_module/ffi_test.py` that:
   - Uses `ctypes` to load `libmathops.so`.
   - Allocates an input array of 100,000 `float` values (32-bit floating point), linearly spaced from `0.0` to `10.0` inclusive (i.e., `x[0]=0.0`, `x[99999]=10.0`).
   - Allocates an output array of 100,000 `float` values.
   - Calls the C function `void compute_poly(const float* input, float* output, int size)` to populate the output.
   - Writes the output array to `/home/user/result.txt`, one float per line, formatted to 4 decimal places.

Generate the output file completely to verify the integration.
You have inherited an unfamiliar codebase for a geographic calculations library. The project is located at `/home/user/geo_project`.

Recently, users have reported that the core function, `compute_chord_length(theta)`, in the module `/home/user/geo_project/geo_math.py` returns inaccurate results—specifically `0.0`—for extremely small angles, even though the distance should be greater than zero. The original developer wrote a mathematically standard formula, but it suffers from catastrophic cancellation (a floating-point precision issue) on x86/x64 systems.

Your objective is to diagnose, test, and repair this codebase by following these steps:

1. **Fuzz Testing Validation**: 
   Write a fuzzing script at `/home/user/geo_project/fuzzer.py`. This script should randomly generate 10,000 values for `theta` in the range `[1e-10, 1e-7]`. It should pass these to `compute_chord_length(theta)`. If the function evaluates to `0.0` (which is incorrect for `theta > 0`), the script should print `BUG FOUND: <theta>` and exit immediately with code 1.

2. **Assertion-based Intermediate Validation**:
   Modify `/home/user/geo_project/geo_math.py`. At the very beginning of the `compute_chord_length(theta)` function, add the following exact assertions to fail fast on invalid inputs:
   - `assert isinstance(theta, float), "theta must be a float"`
   - `assert theta >= 0.0, "theta must be non-negative"`

3. **Formula Correction & Precision Repair**:
   Fix the implementation of `compute_chord_length(theta)` in `/home/user/geo_project/geo_math.py` so that it avoids catastrophic cancellation. You must replace the existing naive formula with a mathematically equivalent formula that remains precise for values of `theta` near zero (Hint: use a half-angle trigonometric identity).

4. **Final Verification**:
   Once you have completed the fuzzing script, added the assertions, and fixed the floating-point precision issue, run the provided verification script:
   `python3 /home/user/geo_project/verify.py`
   If successful, it will generate a file `/home/user/geo_project/success.txt`. Leave this file intact, as it will be used to verify your success.
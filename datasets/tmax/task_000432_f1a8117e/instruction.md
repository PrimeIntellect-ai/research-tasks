We are porting a numerical analysis tool to run inside a highly minimal, locked-down Linux container. This container lacks traditional utilities like `bc`, `awk`, or `python` for math operations, leaving us only with pure Bash built-in arithmetic. 

Your task is to implement a pure-Bash rational number arithmetic library and a property-based test suite to verify it.

**Step 1: The Library**
Create a Bash script at `/home/user/rational.sh` that provides two functions: `add_rat` and `mul_rat`.
- Both functions must take exactly 4 integer arguments: `N1`, `D1`, `N2`, `D2`, representing two rational numbers `N1/D1` and `N2/D2`.
- `add_rat` must compute the sum of the two rational numbers.
- `mul_rat` must compute the product of the two rational numbers.
- Both functions must `echo` the result strictly in the format `N/D`, reduced to its lowest terms (e.g., `1/2`, not `2/4`).
- `D` must always be strictly positive. If the resulting value is negative, the minus sign must be on the numerator `N` (e.g., `-3/4`, not `3/-4`). If the result is zero, output `0/1`.
- You must write a helper function inside the script to compute the Greatest Common Divisor (GCD) to reduce the fractions.

**Step 2: Property-Based Testing**
Create a test script at `/home/user/test_rational.sh` that verifies the commutative property of addition for your library.
- It must source `/home/user/rational.sh`.
- It must generate exactly 100 sets of random integer arguments for `N1`, `D1`, `N2`, `D2` (where `D1` and `D2` are strictly non-zero, randomly chosen between -50 and 50, and `N1`, `N2` between -50 and 50).
- For each set, it must check if `add_rat N1 D1 N2 D2` produces the exact same string output as `add_rat N2 D2 N1 D1`.
- If any test fails, it should immediately exit with code 1.
- If all 100 tests pass, it must write the exact string `ALL_PASS` to `/home/user/test_result.log` and exit with code 0.

Ensure your scripts use strict Bash arithmetic `(( ))` or `$(( ))` without invoking external binaries for the math.
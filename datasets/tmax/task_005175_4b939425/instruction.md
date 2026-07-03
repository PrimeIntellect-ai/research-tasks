You are the on-call engineer and just received a PagerDuty alert at 3:00 AM. The nightly financial risk pipeline has crashed. 

The application is located in `/home/user/risk_engine`. 

Here is what the previous engineer noted before their laptop died:
1. "The nightly batch job is failing because the `calc_variance` executable isn't building. Someone pushed a bad commit that causes a compiler/linker error when running `./build.sh`."
2. "Even if you fix the build, the calculation algorithm was recently 'optimized' but it's now suffering from severe numerical instability (catastrophic cancellation), resulting in `NaN` outputs for our high-precision floating-point datasets. The code reads floats from `data.txt` and calculates their standard deviation. You need to fix the algorithm so it calculates the standard deviation accurately without returning NaN."
3. "The API endpoint requires a calibration secret to submit the final results. The secret was accidentally hardcoded in an early commit, but later removed and replaced with an environment variable. We don't have it written down anywhere. You'll need to dig through the git history of the repository to find the original secret string."

Your task:
1. Navigate to `/home/user/risk_engine`.
2. Recover the deleted calibration secret from the Git repository's history.
3. Fix the build script (`build.sh`) and/or code (`calc_variance.c`) so it compiles successfully. (You may also completely rewrite the tool in the language of your choice, provided it compiles/runs via `./build.sh`, produces an executable named `calc_variance`, and reads `data.txt` to output the standard deviation to stdout).
4. Fix the numerical instability in the standard deviation calculation (e.g., use Welford's algorithm or a two-pass approach). 
5. Run the fixed executable on `data.txt`.
6. Write the results to `/home/user/resolution.log` in EXACTLY the following format:

```
SECRET: <recovered_secret_string>
STDDEV: <calculated_standard_deviation_to_4_decimal_places>
```

The fate of tomorrow's trading day rests on you resolving this page. Good luck.
You are a Systems Data Scientist working on a low-level data processing pipeline in C. We have encountered an issue where our datasets occasionally contain silent corruption (e.g., text like "NaN", "N/A", or extreme outliers in integer columns) which silently converts to `0` when parsed by standard C functions, wreaking havoc on our downstream statistical models.

We rely on a proprietary third-party C library for tokenization and basic stats, located at `/app/vendored/libstatscsv-1.0`. 

Your objectives are:

1. **Fix the Vendored Library**
   The library `libstatscsv-1.0` currently fails to compile due to a broken `Makefile` and a missing header import in its source. You must diagnose and fix the compilation errors so that `make` successfully builds `libstatscsv.a`.

2. **Implement an Adversarial Data Detector**
   Write a C program located at `/home/user/detector.c` (and compile it to `/home/user/detector`). Your program must link against the fixed `libstatscsv.a` and use its tokenization primitives.
   
   The `detector` program must take a single command-line argument: the path to a CSV file.
   It should exit with code `0` if the dataset is "clean" and code `1` if the dataset is "evil".

   A dataset is considered **evil** (and must be rejected) if:
   - The "score" column contains any missing value representations (e.g., "NaN", "N/A", or empty strings). You must detect these *before* they are silently converted to `0` or other numeric defaults.
   - OR, after valid parsing, the dataset contains extreme outliers. To determine this, implement a bootstrap method (1000 resamples, with replacement) to calculate the 95% confidence interval of the mean of the "score" column. If the lower bound of the 95% CI is less than `45.0` or the upper bound is greater than `55.0`, the dataset is evil.

   A dataset is considered **clean** (and must be accepted) if it contains valid integer tokens and its bootstrap 95% CI falls entirely within the `[45.0, 55.0]` range inclusive.

   *Note: The CSV files have a header row. You should only process the "score" column.*

3. **Test Against the Corpus**
   We have provided two directories of test data:
   - `/app/corpus/clean/` (contains only clean datasets)
   - `/app/corpus/evil/` (contains datasets with injected NaNs or extreme outliers)
   
   Your compiled `/home/user/detector` must exit `0` for 100% of the files in the `clean` directory, and exit `1` for 100% of the files in the `evil` directory.

Write your code efficiently and ensure it correctly handles the logic and exit codes.
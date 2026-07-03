You have inherited an unfamiliar Python codebase located at `/home/user/astro_calc`. This library is used for astronomical calculations, particularly computing the Julian Date from Gregorian datetimes. 

Recently, the test suite (`test_jd.py`) has started failing. A subtle bug was introduced somewhere in the git history. 

Your task consists of the following steps:
1. **Error Diagnosis & Git Forensics:** Use `git` (e.g., `git bisect`) to identify the exact commit hash that introduced the bug breaking `test_jd.py`. Write the full, 40-character commit hash to `/home/user/bug_commit.txt`.
2. **Secret Recovery:** During your git history forensics, you will notice that a secret token was accidentally committed in a configuration file and later removed. Find this token and write the literal token string to `/home/user/secret.txt`.
3. **Formula Correction:** Fix the algorithmic bug in `jd.py` so that `test_jd.py` passes. The bug is a subtle mathematical error in the implementation of the formula.
4. **Execution:** Once fixed, calculate the Julian Date for `2024-01-01 12:00:00` (UTC) using the corrected `get_julian_date` function in `jd.py`. Write the resulting float value to `/home/user/jd_output.txt`.

Ensure your fixes are in `/home/user/astro_calc/jd.py` and the outputs match exactly.
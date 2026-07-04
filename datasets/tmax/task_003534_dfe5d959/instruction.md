You are an IT support technician. We just received an urgent ticket (TICKET-8821) from the observability team. 

The background metrics service at `/home/user/metric_service` is currently reporting incorrect "System Health Scores". The team notes that the average health score used to reliably output around `83.71` based on the static test dataset, but recently it has been outputting a much lower, incorrect value. 

The service is a Python script named `calc.py`. It appears a recent commit introduced a mathematical error in the core formula implementation.

Your task is to:
1. Use `git bisect` (or manual tracing of the git history) in the `/home/user/metric_service` repository to find the exact commit that introduced the regression. The first commit in the repository is known to be good.
2. Identify the formula implementation error introduced in that bad commit.
3. Fix the formula in the current `calc.py` (HEAD) to restore the correct calculation logic.
4. Add temporary intermediate state tracing (print statements) to verify the individual health scores for each data point if you need to, but the final printed output of `calc.py` must be the correct "Final Average".
5. Write your findings to a log file at `/home/user/resolution.txt` in the following exact format:

```
BAD_COMMIT=<full_40_char_git_hash>
CORRECTED_AVERAGE=<value_rounded_to_2_decimal_places>
```

Ensure the repository remains in a clean working state (abort any bisect operation once finished, and leave the fixed `calc.py` uncommitted or committed as you see fit, but the file must be corrected).
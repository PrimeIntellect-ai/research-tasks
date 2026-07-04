You are a DevOps engineer debugging a failing data analytics job.

The repository containing the job is located at `/home/user/analytics`. 
Currently, when you run `python3 /home/user/analytics/score.py`, it outputs `[nan nan nan]` because of a numerical instability issue (an overflow during exponentiation) triggered by the input data. 

Additionally, an automated security scanner has flagged that a database password was accidentally committed somewhere in the git history of this repository before being removed. 

Your tasks are to:
1. Analyze the git history of `/home/user/analytics` and recover the leaked database password (it was assigned to the variable `DB_PASS`).
2. Fix the numerical instability in `/home/user/analytics/score.py` by implementing a numerically stable version of the softmax function (e.g., using the shift-invariant property `x - max(x)`).
3. Run the fixed `score.py` to calculate the correct output array.
4. Create a JSON file at `/home/user/report.json` containing the recovered password and the first value of the fixed softmax output array, rounded to exactly 4 decimal places.

The JSON file at `/home/user/report.json` must strictly follow this exact schema:
```json
{
  "db_password": "the_leaked_password",
  "softmax_first_value": 0.1234
}
```

Make sure the required libraries (like `numpy`) are installed or install them via `pip` if needed.
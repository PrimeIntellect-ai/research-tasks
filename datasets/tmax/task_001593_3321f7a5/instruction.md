You are a data analyst working with user profile data. We need a fast command-line tool to find the most similar candidate for a given user based on their profile features.

You have two CSV files:
1. `/home/user/users.csv`: Contains user profiles with columns `id,age,score1,score2`.
2. `/home/user/candidates.csv`: Contains candidate profiles with columns `cand_id,age,score1,score2`.

Your task is to write a Bash script located at `/home/user/find_match.sh` that takes a single user `id` as an argument. The script should:
1. Extract the profile for the given user from `users.csv`.
2. As a feature engineering step, scale `score1` by multiplying it by 10 for both the user and all candidates.
3. Compute the squared Euclidean distance between the user and all candidates using the features: `age`, the scaled `score1`, and `score2`.
4. Output ONLY the `cand_id` of the candidate with the smallest distance to standard output.

Example usage:
```bash
bash /home/user/find_match.sh U100
```
This should print just the `cand_id` (e.g., `C3`).

Notes:
- The script must be written in Bash (using standard UNIX tools like `awk`, `grep`, `sed`, etc. is perfectly fine and encouraged).
- Do not output anything else (no debugging text) to standard output.
- You can assume valid input and that the user ID exists in the file.
- The CSV files have headers.
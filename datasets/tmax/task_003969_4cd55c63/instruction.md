I have a Rust repository located at `/home/user/math_repo` that contains some critical numerical calculations for our scientific pipeline. 

Recently, our CI pipeline started failing intermittently on the test suite. We suspect a numerical instability (catastrophic cancellation or precision loss) was introduced somewhere in the last 200 commits, but because the test relies on random sampling, it only fails about 20% of the time. 

Your task is to:
1. Diagnose the intermittent failure and write a script or use a loop to reliably reproduce it.
2. Use `git bisect` (or another forensic method) to identify the exact commit hash that introduced the buggy, unstable numerical code.
3. While you are digging through the git history, I also need you to recover a lost secret. An admin token (formatted like `ADMIN_TOKEN="..."`) was accidentally committed early in the repository's history and removed shortly after. Please find this token.

Once you have found both the commit hash that introduced the bug and the admin token, write them to a file named `/home/user/debugging_report.txt` in the following exact format:

```text
BAD_COMMIT=<full_40_character_commit_hash>
ADMIN_TOKEN=<token_value>
```

Replace `<full_40_character_commit_hash>` with the full git commit hash that introduced the regression, and `<token_value>` with the string value of the secret token.
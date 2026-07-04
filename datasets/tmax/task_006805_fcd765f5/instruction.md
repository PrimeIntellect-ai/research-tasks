You have been given access to a Git repository located at `/home/user/math_repo`.

This repository contains a Python script `analyze.py` which computes the median of a list of numbers provided in a text file. Recently, a regression was introduced somewhere in the commit history: the script now crashes when trying to process any file that has a space in its filename.

Your objectives are:
1. Use `git bisect` (or any other method) to identify the exact commit hash that introduced this regression. Write the full 40-character commit hash to `/home/user/bad_commit.txt`. The initial commit in the repository is known to be "good", and the latest commit (HEAD) is "bad".
2. While investigating the git history, you may notice that a developer accidentally committed an API key (a string starting with `AKIA...`) in a file named `config.json`, which was removed in a later commit. Find this API key and write it to `/home/user/secret.txt`.

Ensure your final output files contain nothing but the requested strings.
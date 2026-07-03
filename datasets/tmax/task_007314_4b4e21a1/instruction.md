You are tasked with debugging a regression in a machine learning utility repository located at `/home/user/ml_tools`. 

The repository contains a Python script, `softmax.py`, which reads a JSON list of floats from a file and outputs their softmax probabilities as a JSON list. 
Recently, a commit introduced a numerical instability regression. When run on datasets with large numbers, such as the one at `/home/user/eval data/large_inputs.json`, the script now crashes with an `OverflowError` instead of producing valid probabilities.

The `main` branch currently has 200 commits. It is known that `HEAD~150` is a "good" commit, while `HEAD` is "bad".

Your objectives are:
1. Use `git bisect` to identify the exact commit hash that introduced the regression. 
   *Hint: If you write a bash script to automate the bisection with `git bisect run`, ensure it correctly handles the space in the directory name `"eval data"`.*
2. Write the full 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.
3. Check out the `main` branch. Diagnose and fix the numerical instability in `/home/user/ml_tools/softmax.py`. To make the softmax computation numerically stable, subtract the maximum value of the input array from each element before exponentiating.
4. Run your fixed `softmax.py` against `/home/user/eval data/large_inputs.json` and redirect its standard output to `/home/user/fixed_output.txt`. The output should be a valid JSON array of floats.
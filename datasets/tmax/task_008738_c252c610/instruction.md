You are a support engineer tasked with collecting diagnostics for a mathematical library used by our clients. A customer reported that the Markov Chain steady-state solver in our `markov_solver` library recently started diverging, producing state vectors that no longer sum to 1.0 (violating the law of total probability). 

The repository is located at `/home/user/markov_solver`.
The known good release is tagged as `v1.0`. The current `main` branch is failing.

Your task is to:
1. Use `git bisect` to identify the exact commit that introduced the bug. Use `python test_solver.py` to test whether a commit is good or bad.
2. Once you find the bad commit, check it out.
3. The customer needs to know exactly when the numerical instability begins in the bad commit. Modify `solver.py` (or inject assertions/logging) to trace the intermediate state of the vector at each iteration. Find the *first* iteration number (0-indexed, where the initial state before any transitions is iteration 0, and the state after the first transition is iteration 1) where the sum of the `state` vector drops below `0.99`.
4. Create a diagnostic report at `/home/user/diagnostics.txt` with the following strict `KEY=value` format:

```
BAD_COMMIT=<full_40_character_git_hash>
DIVERGENCE_ITERATION=<integer_iteration_number>
```

Ensure your final output is exclusively in `/home/user/diagnostics.txt` as specified.
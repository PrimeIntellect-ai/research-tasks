You are tasked with diagnosing a regression in a mathematical simulation repository located at `/home/user/math_repo`. 

The simulation script `sim.py` has been failing intermittently in production. We know that the failure is a rare mathematical edge case (a division by zero during a matrix transformation) that is only triggered by specific random states. 

During early debugging months ago, a developer found a specific RNG seed that reliably triggers this failure. They temporarily committed it to the repository in a file named `debug_seed.txt`, but shortly after, the file was deleted to clean up the repository. Since then, the simulation logic has been heavily modified across hundreds of commits, and a regression was introduced somewhere.

Your objectives:
1. **Forensics**: Search the git history of `/home/user/math_repo` to find the deleted `debug_seed.txt` file and extract the exact seed value. Save this integer seed to `/home/user/recovered_seed.txt`.
2. **Reproduction & Bisection**: The script can be run with `python sim.py --seed <SEED_VALUE>`. Using the recovered seed, the script will crash (exit code 1) *only if* the regression is present. 
3. Run a `git bisect` to find the exact commit that introduced the bug. The `main` branch HEAD is currently broken (bad). The tag `v1.0` is known to be working (good).
4. Save the full 40-character commit hash of the *first bad commit* (the one that introduced the regression) to `/home/user/bad_commit_hash.txt`.

Ensure your final state has both `/home/user/recovered_seed.txt` and `/home/user/bad_commit_hash.txt` correctly populated.
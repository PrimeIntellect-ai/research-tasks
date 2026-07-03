You are tasked with debugging a regression in a physics simulation project.

A local Git repository is located at `/home/user/simulation_repo`. The repository contains 200 commits. The main simulation script is `sim.py`. 

Recently, a regression was introduced that causes the simulation to fail due to a strict floating-point equality check instead of a proper tolerance-based check. The script is designed to exit with `0` on success and a non-zero exit code on failure. 

However, there is an environment misconfiguration: the `sim.py` script requires a secret key to run, which must be provided via the `SIM_SECRET_KEY` environment variable. If this variable is missing or incorrect, the script will crash before even running the simulation. We know that the configuration file containing this secret (in JSON format) was accidentally committed early in the repository's history and subsequently deleted.

Your objectives:
1. Search the git history of `/home/user/simulation_repo` to recover the deleted `SIM_SECRET_KEY`.
2. Save the exact value of the recovered secret key to `/home/user/secret.txt`.
3. Set the environment variable so you can run the script.
4. Bisect the repository to find the exact commit hash that introduced the floating-point precision regression. The tag `v1.0` is known to be a "good" state, while the current `HEAD` is "bad".
5. Save the full 40-character commit hash of the first bad commit to `/home/user/bad_commit.txt`.

Ensure your final answers are saved exactly to the paths specified.
I need your help debugging a mathematical regression in our data processing pipeline. 

We have a Git repository located at `/home/user/repo` which contains a script `process.sh` and a data file `data.b64`. The script reads base64 encoded floating-point data, decodes it, and performs a series of calculations (summing the inverses of the numbers). 

Recently, we noticed that the final output has suffered a severe precision loss. The `main` branch currently outputs a heavily truncated or rounded number compared to the original version. I know the initial commit (which you can find at the root of the commit history) was perfectly accurate. There are exactly 200 commits in this repository.

Your task:
1. Use `git bisect` (or any other method) to find the first commit that introduced the precision loss regression. The regression is defined as the first commit where the output of `./process.sh` differs from the output of the very first commit.
2. Write the full 40-character SHA-1 hash of this first bad commit to `/home/user/bad_commit.txt`.
3. Checkout the `main` branch and fix the precision bug in `process.sh`. The script must correctly decode the data and calculate the result without truncating the intermediate floating-point operations. Keep the high precision (e.g., `scale=7` if using `bc`).
4. Run the fixed `./process.sh` on the `main` branch and save the final numerical output to `/home/user/fixed_output.txt`.

Ensure your fixes are applied to the `main` branch, and the output format in `/home/user/fixed_output.txt` is just the raw number.
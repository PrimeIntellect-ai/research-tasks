I am a data scientist fitting models and need to calculate the distance between probability distributions to tune my parameters. I have two discrete probability distributions saved in `/home/user/P.txt` and `/home/user/Q.txt`. Each file contains one probability value per line, representing $P_i$ and $Q_i$ respectively.

Your tasks are to:
1. Write a Bash script at `/home/user/calc_kl.sh` that takes two file paths as arguments (first P, then Q). The script must compute the Kullback-Leibler (KL) divergence $D_{KL}(P || Q) = \sum P_i \ln(P_i / Q_i)$ using `awk`, and print only the resulting value rounded to exactly 5 decimal places.
2. Execute your script on `/home/user/P.txt` and `/home/user/Q.txt` and save the output to `/home/user/kl_out.txt`.
3. I also need to find the parameter $x$ that satisfies the nonlinear equation $x^3 - x - D_{KL} = 0$, where $D_{KL}$ is the exact unrounded KL divergence computed from the first step. Write a second Bash script at `/home/user/find_root.sh` that finds the real root of this equation in the interval $[1, 2]$. You can use `awk` or `bc` to implement a simple root-finding algorithm (like bisection or Newton-Raphson). The script should print the root rounded to exactly 5 decimal places.
4. Execute `/home/user/find_root.sh` and save its output to `/home/user/root_out.txt`.

Ensure both scripts have executable permissions. Use only standard shell built-ins, `coreutils`, `awk`, and `bc`.
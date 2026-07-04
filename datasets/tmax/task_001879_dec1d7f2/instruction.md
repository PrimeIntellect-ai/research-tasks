You are a bioinformatics analyst studying the population dynamics of a wild-type allele in a tumor cell culture. 

You have a Bash script at `/home/user/simulate_allele.sh` that numerically integrates an Ordinary Differential Equation (ODE) representing the allele fraction over time:
$dW/dt = -m \cdot W + b \cdot W \cdot (1 - W)$
where $m$ is the mutation rate and $b=2.0$ is the constant birth rate. The simulation runs from $t=0$ to $t=10$ with an initial condition of $W(0) = 0.99$.

Currently, the script uses a fixed time step (`dt=0.5`), which is too large. The explicit Euler integration diverges, resulting in negative allele fractions.

Your objectives:
1. **Refine the time mesh:** Modify `/home/user/simulate_allele.sh` so that the default time step `dt` is `0.01` instead of `0.5`. Do not change the underlying ODE logic or the integration method.
2. **Optimize the parameter:** Write a new Bash script at `/home/user/optimize_m.sh`. This script must perform a grid search over the mutation rate $m$ from `1.00` to `2.50` inclusive, in increments of `0.01`. It should call `./simulate_allele.sh <m> 0.01` for each value.
3. Find the **smallest** mutation rate $m$ (to two decimal places) such that the final allele fraction $W(10)$ is strictly less than `0.1000`.
4. **Log the result:** Save the optimal $m$ and its corresponding $W(10)$ output to `/home/user/result.txt` in exactly this format:
   `m=<value>, W=<value>`

Ensure your optimization script is executable and uses standard Bash tools (like `awk`, `bc`, or `seq`).
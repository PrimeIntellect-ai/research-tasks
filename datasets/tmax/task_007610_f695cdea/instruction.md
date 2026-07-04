You are a researcher investigating the convergence properties of a new stochastic numerical integrator. The integrator is supposed to sample from a target distribution, which is theoretically a Gaussian with mean $\mu_{target} = 2.0$ and standard deviation $\sigma_{target} = 2.0$. 

Due to a suspected bug in the step-size adaptation, the integrator diverges from the true distribution depending on the step size $dt = 1/N$, where $N$ is the number of steps. 

You have run the simulation for $N \in \{10, 20, 40, 80\}$. The final states of 10,000 independent particles for each $N$ have been saved in the following files:
- `/home/user/sim_10.txt`
- `/home/user/sim_20.txt`
- `/home/user/sim_40.txt`
- `/home/user/sim_80.txt`

Your task is to write and run a **C program** that calculates the order of convergence of the error. Specifically, your program must:

1. Read the particle states from each of the 4 text files.
2. For each file, compute the empirical population mean ($\hat{\mu}$) and empirical population standard deviation ($\hat{\sigma}$). (Use $M=10000$ as the denominator for variance: $\hat{\sigma} = \sqrt{\frac{1}{M} \sum_{i=1}^M (x_i - \hat{\mu})^2}$).
3. Calculate the squared 2-Wasserstein distance $D$ between the empirical normal distribution $\mathcal{N}(\hat{\mu}, \hat{\sigma}^2)$ and the target distribution $\mathcal{N}(2.0, 2.0^2)$. Use the simplified formula for Gaussians: 
   $D = (\hat{\mu} - \mu_{target})^2 + (\hat{\sigma} - \sigma_{target})^2$
4. Perform a linear least-squares regression to fit the line $\ln(D) = m \cdot \ln(dt) + c$, where $dt = 1/N$.
5. Determine the slope $m$ (which represents the convergence order).
6. Save the calculated slope $m$ to the file `/home/user/convergence_order.txt`, formatted to exactly three decimal places (e.g., `1.842`).

Ensure your code is written in C and can be compiled and executed using standard tools available in a Linux environment (e.g., `gcc`).
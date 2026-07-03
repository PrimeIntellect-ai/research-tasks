You are assisting a researcher who is dealing with non-reproducible simulation results caused by floating-point reduction order variations in an external black-box simulator. The researcher needs to robustly extract a system parameter $k$ from a noisy, fragmented log file produced by the simulator.

The raw simulation data is located at `/home/user/sim_output.log`. The file contains interleaved log messages. The relevant data points are split across different lines, where time `t` and the corresponding signal value `val` are logged sequentially but separated by debug messages. 
For example:
```
[INFO] t=0.0
[DEBUG] calc step 0
[DATA] val=0.0000
[INFO] t=0.1
[DEBUG] calc step 1
[DATA] val=0.3894
...
```

Your task is to write a Bash script (using standard tools like `awk`, `sed`, `grep`, `bc`) to perform the following pipeline:

1. **Observational Data Reshaping:** Parse `/home/user/sim_output.log` to extract the corresponding `t` and `val` pairs into a clean tabular/paired format.

2. **Spectral Analysis (DFT):** The signal oscillates at a dominant integer frequency $\omega_{max}$. Using Bash and/or `awk`, compute the unnormalized Discrete Fourier Transform power $P(\omega)$ for integer frequencies $\omega \in \{1, 2, 3, 4, 5, 6\}$. 
The power is defined as:
$P(\omega) = \left( \sum_{i} \text{val}_i \cos(\omega t_i) \right)^2 + \left( \sum_{i} \text{val}_i \sin(\omega t_i) \right)^2$
Identify the frequency $\omega_{max}$ that yields the maximum power $P(\omega)$.

3. **Nonlinear Equation Solving:** The dominant frequency $\omega_{max}$ is tied to the physical parameter $k$ via the nonlinear equation:
$k + e^{-k} = \omega_{max}^2$
Implement a Newton-Raphson solver in your script (using `awk` or `bc`) to find the value of $k$.
Use the function $f(k) = k + e^{-k} - \omega_{max}^2$.
Start with an initial guess of $k_0 = 1.0$ and perform exactly 5 Newton-Raphson iterations. 

Save the final computed value of $k$ after 5 iterations to `/home/user/result.txt`, formatted to exactly four decimal places (e.g., `9.0000`).

Ensure all calculations and reshaping are done via Bash shell scripting/commands. Do not use Python, R, or compiled languages for this task.
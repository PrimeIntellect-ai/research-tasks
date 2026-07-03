You are a researcher modeling a biological population. The population grows according to the differential equation $dy/dt = -0.1 y^2 + 0.5 y$. However, the initial population $y(0)$ is uncertain. You have a small dataset of empirical initial population measurements, and you need to estimate the 95% confidence interval for the median of the population at time $t=5$.

Write a Go program at `/home/user/simulate.go` that performs the following steps:

1. **Distribution Fitting**:
   Read the empirical data from `/home/user/data.csv` (which contains one float per line). Calculate the sample mean ($\mu$) and the sample standard deviation ($s$) using the $N-1$ denominator.

2. **Simulation & ODE Solving**:
   Initialize a local random number generator with seed `12345` (i.e., `rng := rand.New(rand.NewSource(12345))`).
   Sample 1000 initial conditions from a Normal distribution $\mathcal{N}(\mu, s^2)$. Draw them sequentially in a loop from $i=0$ to $999$ using `rng.NormFloat64() * s + mu`.
   For each initial condition, solve the ODE $dy/dt = -0.1 y^2 + 0.5 y$ from $t=0$ to $t=5$ using the classic 4th-order Runge-Kutta (RK4) method with a fixed step size of $\Delta t = 0.1$ (50 steps). Save the final population $y(5)$ for each of the 1000 simulations.
   
   *RK4 Equations:*
   $k_1 = f(t, y)$
   $k_2 = f(t + \Delta t / 2, y + \Delta t \cdot k_1 / 2)$
   $k_3 = f(t + \Delta t / 2, y + \Delta t \cdot k_2 / 2)$
   $k_4 = f(t + \Delta t, y + \Delta t \cdot k_3)$
   $y_{new} = y + \frac{\Delta t}{6}(k_1 + 2k_2 + 2k_3 + k_4)$

3. **Bootstrap Confidence Interval**:
   To find the 95% confidence interval of the **median** of $y(5)$, perform 2000 bootstrap iterations.
   In each iteration $b$ (from $0$ to $1999$):
   - Sample 1000 values from your array of final populations with replacement. Generate the indices using `rng.Intn(1000)` sequentially for $j=0$ to $999$.
   - Calculate the median of this bootstrap sample. (Since the sample size is 1000, sort the sample and take the average of the elements at indices 499 and 500).
   - Store this bootstrap median.
   
   After 2000 iterations, sort the bootstrap medians. The 2.5th percentile (lower bound) will be at index 50, and the 97.5th percentile (upper bound) will be at index 1950 of the sorted array.

4. **Output**:
   Write the results to `/home/user/output.txt` in exactly the following format (floats formatted to 4 decimal places):
   ```
   Mean Initial: <mu>
   Std Initial: <s>
   Lower CI: <lower>
   Upper CI: <upper>
   ```

Compile and run your Go program to produce `/home/user/output.txt`.
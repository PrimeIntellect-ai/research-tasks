You are a performance engineer tasked with profiling and validating a thermal model for a new 1D chip architecture. You have empirical sensor data, but you need to write a fast numerical simulator in C to find the optimal integration time step and evaluate the model's accuracy.

Your task is to implement a 1D thermal simulator, perform convergence testing to find a suitable time step, and fit a normal distribution to the error residuals compared to the empirical sensor data.

**1. The Thermal Model (PDE)**
The chip is modeled as a 1D rod of length $L = 1.0$ with thermal diffusivity $\alpha = 0.01$. The heat equation with a power source $P(x)$ is:
$$\frac{\partial u}{\partial t} = \alpha \frac{\partial^2 u}{\partial x^2} + P(x)$$

*   **Spatial Grid:** Use a uniform grid with $\Delta x = 0.1$. The grid points are $x_i = i \cdot \Delta x$ for $i \in \{0, 1, \dots, 10\}$.
*   **Time:** Simulate from $t = 0.0$ to $t = 2.0$.
*   **Initial Condition:** $u(x_i, 0) = 25.0$ for all $i$.
*   **Boundary Conditions:** Fixed ambient temperature at the edges: $u(0, t) = 25.0$ and $u(1.0, t) = 25.0$.
*   **Power Source:** The chip's active cores generate heat. $P(x_i) = 1000.0$ for $i \in \{4, 5, 6\}$ (which correspond to $x = 0.4, 0.5, 0.6$). For all other $i$, $P(x_i) = 0.0$.
*   **Numerical Method:** Use the Explicit Euler method for time integration and central finite differences for the spatial second derivative. 

**2. Convergence Testing**
You must find the optimal time step $dt$.
*   Start with $dt = 0.1$.
*   Run the simulation to $t = 2.0$ and record the center temperature $u(0.5, 2.0)$.
*   Repeatedly halve the time step ($dt_{new} = dt_{old} / 2$) and re-run the simulation.
*   Stop when the absolute difference in the center temperature $u(0.5, 2.0)$ between the current $dt$ and the previous $dt$ is **strictly less than 0.01**. The current $dt$ is your "optimal $dt$".

**3. Density Estimation / Error Fitting**
Empirical sensor readings at $t = 2.0$ are located in `/home/user/sensor_data.txt` (11 lines, corresponding to $x_0$ through $x_{10}$).
Using the final temperature array $u(x_i, 2.0)$ calculated with your *optimal* $dt$:
*   Calculate the error residual for each point: $e_i = u(x_i, 2.0) - S_i$ (where $S_i$ is the sensor reading).
*   Fit a normal distribution to these 11 errors by calculating the population mean ($\mu$) and population variance ($\sigma^2$) of the errors $e_i$ (divide by $N=11$, not $N-1$).

**Output Requirements**
Write your C code in `/home/user/thermal_sim.c`. Compile and run it to produce a JSON file at `/home/user/results.json` with exactly the following structure (replace placeholders with your computed floats, accurate to at least 4 decimal places):

```json
{
  "optimal_dt": 0.0000,
  "center_temp": 0.0000,
  "error_mean": 0.0000,
  "error_variance": 0.0000
}
```
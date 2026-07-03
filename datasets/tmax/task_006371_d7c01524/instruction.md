You are a bioinformatics analyst working with a synthetic biology lab. We are modeling a synthetic genetic oscillator (based on a simplified Goodwin model) and need to analyze its mRNA expression period and total expression using Go.

Your task is to write a Go program (in `/home/user/workspace/analyze_oscillator.go`) that performs the following steps:

1. **ODE Numerical Solving (Simulation)**
   Implement a 4th-order Runge-Kutta (RK4) solver in Go to simulate the following system of Ordinary Differential Equations from $t = 0$ to $t = 200$ with a time step of $dt = 0.1$ (resulting in 2001 points, including $t=0$).
   
   Equations:
   $dx/dt = \frac{1}{1 + z^{10}} - 0.1x$
   $dy/dt = x - 0.1y$
   $dz/dt = y - 0.1z$
   
   Initial conditions: $x(0) = 0.1$, $y(0) = 0.1$, $z(0) = 0.1$.
   Here, $x$ represents the mRNA concentration. Keep track of the $x$ values over the simulation.

2. **Numerical Integration**
   Calculate the total accumulated mRNA expression over the entire simulation window ($t=0$ to $t=200$). Use the composite Simpson's 1/3 rule on the discrete $x$ values you just simulated.

3. **Spectral Analysis (FFT)**
   Perform a Fast Fourier Transform (FFT) on the 2001 $x$ values to find the dominant oscillation frequency. 
   - You may use a library like `gonum.org/v1/gonum/dsp/fourier`.
   - Find the frequency with the maximum amplitude in the magnitude spectrum. 
   - **Ignore the DC component (index 0).** 
   - Calculate the actual frequency in Hz (assuming $dt=0.1$ seconds).

4. **Output Results**
   Write the final results to `/home/user/analysis.json` in the following exact format:
   ```json
   {
       "total_mrna_integral": 123.4567,
       "dominant_frequency_hz": 0.01234
   }
   ```

**Constraints & Notes:**
- Initialize your go module in `/home/user/workspace`.
- You may use any open-source Go packages (like `gonum`).
- Ensure your output values are highly accurate. Use `float64` for all calculations.
- Your Go script must be compilable and executable to generate the JSON file.
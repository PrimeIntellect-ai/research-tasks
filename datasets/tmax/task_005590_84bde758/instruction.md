You are acting as a computational chemistry researcher. You have been given experimental data measuring the concentration of a chemical intermediate 'B' over time in a reaction. You need to write a C program to numerically simulate two competing kinetic hypotheses, compare them to the experimental data, perform a statistical selection, and visualize the results.

The experimental data is located at `/home/user/experiment.csv`. It contains two columns: Time (t) and Concentration of B ([B]).

**Hypothesis 1 (H1) - First Order:**
dA/dt = -k1 * A
dB/dt = k1 * A - k2 * B
dC/dt = k2 * B

**Hypothesis 2 (H2) - Second Order:**
dA/dt = -k1 * A^2
dB/dt = k1 * A^2 - k2 * B
dC/dt = k2 * B

**Simulation Parameters:**
- Rate constants: k1 = 0.5, k2 = 0.2
- Initial conditions at t = 0: A = 1.0, B = 0.0, C = 0.0
- Time range: t = 0.0 to t = 10.0
- Numerical Method: Euler method
- Step size (dt): 0.001

**Your tasks:**
1. Write a C program at `/home/user/simulate.c`. This program must simulate both H1 and H2 using the Euler method with the exact parameters above.
2. For each hypothesis, extract the simulated concentration of B at the exact time points present in `/home/user/experiment.csv` (which are integers t=0, 1, 2, ..., 10). 
3. Calculate the Mean Squared Error (MSE) between the experimental [B] and the simulated [B] for both hypotheses at these 11 data points.
4. Compile and run your program to generate a file `/home/user/results.txt` with exactly the following format (replace the 0.000000 with your calculated MSEs formatted to 6 decimal places):
```
MSE_H1: 0.000000
MSE_H2: 0.000000
Best: H2
```
(Set "Best: " to either H1 or H2 depending on which has the strictly lower MSE).
5. Output the full time-series simulation data (every step or a sampled subset) to `/home/user/sim_data.csv` so it can be plotted.
6. Use `gnuplot` to create a plot named `/home/user/plot.png` that overlays the experimental data points (as points) and the two simulated curves for [B] (as lines). 

Assume `gnuplot` and standard C compilers (`gcc`) are already installed. You may create any intermediate scripts you need.
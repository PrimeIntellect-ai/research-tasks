You are an AI assistant helping a data scientist fit a kinetic model for a series of chemical reactors. 

We have a network of 3 reactors operating at steady state. A fluid flows from Reactor 0 to Reactor 1, and then to Reactor 2. The flow rate is 1 L/s. 
Reactor 0 is a source with a constant concentration $C_0 = 10.0$ mol/L.
In Reactors 1 and 2, a second-order chemical reaction occurs: $Rate = k \cdot C^2$ (where $k$ is the unknown kinetic rate constant).

The steady-state mass balance equations for the network are:
Reactor 1: $C_0 - C_1 - k \cdot C_1^2 = 0$
Reactor 2: $C_1 - C_2 - k \cdot C_2^2 = 0$

You need to determine the optimal value of $k$ ($k > 0$) by fitting it to observed spectral data.

**Step 1: Signal Processing**
The file `/home/user/spectra.csv` contains raw spectroscopic data for Reactors 1 and 2. 
Columns: `Wavelength` (nm), `Intensity_1`, `Intensity_2`.
The concentration in each reactor ($C_{obs,1}$ and $C_{obs,2}$) is exactly equal to the area under its respective intensity curve between 400 nm and 500 nm. Calculate these observed concentrations by integrating the data (use the trapezoidal rule).

**Step 2: Non-linear Equation Solving & Optimization**
Write a Python script to find the optimal rate constant $k$ that minimizes the sum of squared errors between the observed concentrations and the theoretical concentrations predicted by the mass balance equations:
$SSE = (C_1(k) - C_{obs,1})^2 + (C_2(k) - C_{obs,2})^2$

For any given $k$, you will need to solve the non-linear mass balance equations to find $C_1(k)$ and $C_2(k)$.

**Step 3: Output**
Save your final computed values in a JSON file at `/home/user/results.json` with the following format:
```json
{
  "C_obs_1": 0.0000,
  "C_obs_2": 0.0000,
  "k": 0.0000
}
```
Round all values to 4 decimal places.

Your task is complete once the `results.json` file is accurately populated.
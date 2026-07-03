You are a performance engineer analyzing the thermal characteristics of a heavily loaded scientific computing cluster. You suspect there is a periodic thermal throttling issue affecting one of the CPU cores. 

You have been given a raw observability dataset at `/home/user/thermal_profile.txt`. This file is a space-separated matrix. Each row represents a time step ($\Delta t = 1$ second). The columns are:
`TimeStep  SensorA_Temp  SensorB_Temp  SensorC_Temp  FanSpeed`

Your goal is to write a purely Bash and Awk based pipeline to analyze this data without relying on Python, R, or compiled languages. 

Specifically, you must do the following:

1. **Extract Data:** Extract the `SensorB_Temp` (3rd column) values. The total number of rows is $N$. Let these actual temperature readings be $A_n$ for $n = 0, 1, \dots, N-1$.

2. **Numerical ODE Solving:** The expected temperature $E_n$ follows Newton's Law of Cooling, which can be modeled with the differential equation $\frac{dE}{dt} = -k(E - T_{env})$. 
   Write an `awk` script to numerically solve this using the Forward Euler method:
   $E_{n+1} = E_n - k \cdot (E_n - T_{env}) \cdot \Delta t$
   - Use $k = 0.05$.
   - Use ambient temperature $T_{env} = 25$.
   - The initial expected temperature $E_0$ is exactly equal to the first reading of Sensor B ($A_0$).
   - Compute $E_n$ for all $N$ steps.

3. **Signal Processing (Residuals & Spectral Analysis):**
   - Calculate the residual signal: $R_n = A_n - E_n$.
   - We need to find if there is a dominant periodic throttling frequency. Calculate the magnitude of the Discrete Fourier Transform (DFT) for the target frequency index $k_{freq} = 2$.
   - The DFT magnitude at index $k_{freq}$ is defined as $\sqrt{Re^2 + Im^2}$, where:
     $Re = \sum_{n=0}^{N-1} R_n \cos\left(\frac{2 \pi k_{freq} n}{N}\right)$
     $Im = \sum_{n=0}^{N-1} R_n \sin\left(\frac{-2 \pi k_{freq} n}{N}\right)$
   *(Note: Awk provides `cos()` and `sin()` functions which operate in radians).*

4. **Output:** 
   Calculate the final DFT magnitude for $k_{freq} = 2$ and save it to `/home/user/spectral_result.txt`.
   Format the output to exactly 3 decimal places (e.g., `4.567`).

**Constraints:**
- You must accomplish this using shell utilities (like `bash`, `awk`, `bc`, `sed`, `grep`, etc.).
- Do not use Python, Perl, or any external math libraries.
- Ensure your script cleanly handles the arithmetic and loops.
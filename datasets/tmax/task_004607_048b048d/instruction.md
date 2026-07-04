I am running a simulation of a biological rhythmic process modeled by the Van der Pol oscillator, but my current scripts keep hanging or crashing with numerical errors because the system parameters create a very stiff regime (similar to near-singular matrices in factorization problems).

The system of Ordinary Differential Equations (ODEs) is:
dy/dt = v
dv/dt = mu * (1 - y^2) * v - y

Where:
- `mu = 1000`
- Initial conditions at `t = 0`: `y(0) = 2.0`, `v(0) = 0.0`
- Time span: `t = 0` to `t = 3000`

I need you to write a script (Python, R, or Julia) to:
1. Numerically solve this ODE system over the specified time span. You will need to choose a solver appropriate for highly stiff systems, otherwise the computation will fail or take an eternity.
2. Generate a numerical solution for `y(t)` on a linearly spaced grid of exactly 30,000 points from `t=0` to `t=3000` (inclusive).
3. Compute the numerical integration of `y(t)^2` over this time interval using the trapezoidal rule on those 30,000 grid points. 
4. Save the final integrated value, rounded to exactly 2 decimal places, into `/home/user/result_integral.txt`.

Please execute your script and ensure the output file is created successfully.
You are a data scientist analyzing a biochemical pathway. Your goal is to extract model parameters from a genetic sequence, simulate its corresponding expression dynamics using an ODE model, and compute the total accumulated concentration over time.

Please complete the following steps:

1. Setup Environment: You will need to manage your scientific Python environment. Ensure `numpy`, `scipy`, and `biopython` are installed.
2. Parse Sequence Data: There is a FASTA file located at `/home/user/gene.fasta`. Parse this file to find the sequence length ($L$) and the GC-content ratio ($R$), where $R = (\text{count of G} + \text{count of C}) / L$. 
3. Run ODE Simulation: Simulate the protein concentration $Y(t)$ over time $t$ from $t=0$ to $t=50$. The dynamics are governed by the following Ordinary Differential Equation (ODE):
   $$ \frac{dY}{dt} = -R \cdot Y + \frac{L}{1000} \cdot \cos(t) $$
   With the initial condition $Y(0) = L$.
   Use `scipy.integrate.solve_ivp` with the `RK45` method. You must evaluate the solution at exactly evenly spaced time points from $t=0$ to $t=50$ with a step size of $0.01$ (i.e., $t=0.00, 0.01, 0.02, \dots, 50.00$).
4. Numerical Integration: To find the total accumulated protein over this period, numerically integrate the resulting concentration array $Y(t)$ with respect to time using Simpson's rule (`scipy.integrate.simpson`). Do not use a naive sum, as floating-point reduction errors accumulate over many small steps.
5. Save Result: Write the final integrated area (a single floating-point number) rounded to exactly 3 decimal places to `/home/user/result.txt`.

Ensure your final script runs successfully and produces the file at the requested location.
You are a data scientist analyzing the expression kinetics of a newly sequenced gene. You have a script `/home/user/simulate.py` that reads the sequence from `/home/user/gene.fasta`, calculates its GC content, and uses that to parameterize a system of Ordinary Differential Equations (ODEs) modeling mRNA and Protein production.

The ODEs are:
d[mRNA]/dt = k_tx - k_deg_m * [mRNA]
d[Protein]/dt = k_tl * [mRNA] - k_deg_p * [Protein]

Currently, the script uses a manual Forward Euler numerical integration with a fixed step size (`dt = 0.1`). Because the mRNA degradation rate (`k_deg_m = 1000.0`) is extremely high compared to other rates, the system is stiff. The current step size is too large for the Forward Euler method, causing the integration to wildly diverge and produce `NaN` and `Inf` values.

Your objectives:
1. **Fix the Integration**: Modify `/home/user/simulate.py` to use `scipy.integrate.solve_ivp`. You must choose an appropriate stiff solver (e.g., `BDF` or `Radau`) so the integration successfully completes from `t=0` to `t=10` without diverging. Keep the parameter values and equations exactly the same.
2. **Output the Result**: The script must write the final Protein concentration (at `t=10`) to `/home/user/final_protein.txt`, rounded to exactly 4 decimal places.
3. **Data Visualization**: Generate a plot of Protein concentration vs. time using `matplotlib` and save it as `/home/user/protein_plot.png` within the same script.
4. **Regression Testing**: Write a `pytest` test file at `/home/user/test_simulate.py`. It should test your integration function by supplying a dummy sequence (e.g., "ATGC") or patching the GC calculation, and assert that the final Protein concentration is a valid finite float greater than 0.

Initial files have been placed in `/home/user`. Do not change the ODE parameters. You can modify the functions in `simulate.py` as needed, but ensure running `python3 /home/user/simulate.py` executes the full process.
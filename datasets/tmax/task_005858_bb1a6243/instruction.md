You are a data scientist working on modeling an infectious disease outbreak using the classic SIR (Susceptible-Infected-Recovered) epidemiological model. 

You have been given a Jupyter Notebook `/home/user/analysis.ipynb` that is supposed to:
1. Load daily infection data from `/home/user/data.csv`.
2. Define the SIR system of Ordinary Differential Equations (ODEs).
3. Use a nonlinear least squares optimizer (`scipy.optimize.curve_fit`) to fit the transmission rate (`beta`) and recovery rate (`gamma`) to the observed infected population.
4. Save the fitted parameters to `/home/user/fitted_params.csv`.

However, the current mathematical model implementation is failing our scientific regression tests. The numerical solver explodes or fails to fit the curve properly because there is a fundamental mathematical error in how the ODE system's derivatives are defined in the notebook.

Your task is to:
1. Convert the `/home/user/analysis.ipynb` notebook into a standard Python script named `/home/user/analysis.py`.
2. Locate and fix the mathematical bug in the ODE derivative function inside `analysis.py`. (Hint: Think about the conservation of population and how the Susceptible compartment should change as infections occur).
3. Run the fixed `analysis.py` script to generate the `/home/user/fitted_params.csv` file.
4. Verify your fix by running the regression test suite: `pytest /home/user/test_regression.py`.

The output file `/home/user/fitted_params.csv` must contain exactly one line with the fitted `beta` and `gamma` values separated by a comma, rounded to 4 decimal places (e.g., `0.3521,0.1042`).

Do not change the initial guesses for the optimizer or the initial conditions of the ODE. Only fix the ODE derivative equations.
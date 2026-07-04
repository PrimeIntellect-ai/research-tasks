You are a Machine Learning Engineer preparing a dataset to train a Physics-Informed Neural Network (PINN). The target physical system is modeled by a highly stiff linear Ordinary Differential Equation (ODE). Because of the stiffness, standard explicit numerical solvers can suffer from numerical instability or severe inefficiency, much like matrix factorization algorithms failing on near-singular inputs. 

Before generating the full dataset, you must conduct a numerical stability test to compare explicit and implicit solvers against the exact analytical solution. 

The ODE system is defined as:
dy1/dt = -1000 * y1 + y2
dy2/dt = -y2

Initial conditions at t = 0:
y1(0) = 1.0
y2(0) = 1.0

The analytical solution to this system is known to be:
y1(t) = (998/999) * exp(-1000 * t) + (1/999) * exp(-t)
y2(t) = exp(-t)

Your task is to write and execute a Python script (`/home/user/generate_ode_data.py`) that performs the following steps:

1. Numerically solve the ODE system over the interval t = [0, 1] at 100 evenly spaced points (from t=0 to t=1 inclusive, so t_eval = np.linspace(0, 1, 100)).
   - Use `scipy.integrate.solve_ivp`.
   - Solve it once using the explicit `RK45` method.
   - Solve it again using the implicit `BDF` method.
   - Keep all tolerances at their SciPy defaults.

2. Validate the numerical solutions against the analytical solution:
   - Calculate the analytical solution at the exact same 100 evaluation points.
   - Compute the Mean Squared Error (MSE) between the `RK45` solution and the analytical solution across all points and both variables (i.e., the mean of the squared differences over the 2x100 array).
   - Compute the Mean Squared Error (MSE) between the `BDF` solution and the analytical solution in the same way.

3. Save the results:
   - Create a JSON file at `/home/user/stability_report.json` containing the MSE results with exactly these keys: `{"mse_rk45": <float>, "mse_bdf": <float>}`.
   - Generate the final clean training data by saving the **analytical** solution evaluated at those 100 points to `/home/user/training_data.csv`. The CSV must have a header row `t,y1,y2` and the values should be rounded to exactly 6 decimal places.

Ensure your Python script runs successfully and produces the two required output files.
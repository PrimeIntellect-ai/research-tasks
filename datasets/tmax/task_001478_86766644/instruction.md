I am trying to fit a statistical model to a dataset, but my numerical integration step is causing my optimizer to diverge.

I have a C source file located at `/home/user/integrator.c`. It contains a function with the following signature:
`double integrate(double x, double step_size);`
This function evaluates the integral $\int_0^x e^{-t^2} dt$ using a basic numerical method. 

I also have a dataset at `/home/user/data.csv` containing columns `x` and `y`.
The theoretical model for the data is: $y_i = \int_0^{\mu \cdot x_i} e^{-t^2} dt$.

My goal is to find the optimal parameter $\mu$ that minimizes the Mean Squared Error (MSE) between the model predictions and the true $y_i$ values in the dataset. 

Here is what I need you to do:
1. Compile the `integrator.c` file into a shared library named `/home/user/libintegrator.so`.
2. Write a script in your preferred language to perform the optimization (e.g., using gradient descent or a simplex method like Nelder-Mead) to find the best $\mu$. You must call the compiled C library for the integration step.
3. I previously tried setting `step_size = 0.5`, but the numerical method became highly unstable and caused the optimization to diverge. Perform a convergence test to find a valid `step_size` that allows the integrator to remain stable and accurate.
4. Run the optimization with the stable step size. The initial guess for $\mu$ should be `1.0`.
5. Write the optimal value of $\mu$, rounded to exactly 2 decimal places, into a file at `/home/user/result.txt`. The file should contain only this number (e.g., `1.23`).

Please complete these steps.
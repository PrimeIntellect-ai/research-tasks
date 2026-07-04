You are assisting a bioinformatics analyst who is processing nanopore sequencing signals. The team has developed a custom Go-based tool located in `/home/user/nanofit` that models signal decay over time to identify specific chemical modifications in DNA sequences. The tool uses gradient descent optimization and density estimation to fit theoretical models to the observed data.

However, the tool is currently failing its regression test suite. The core issue lies in the numerical integrator used to evaluate the signal models (`/home/user/nanofit/ode.go`). The integrator simulates an ordinary differential equation (ODE) representing the signal decay. Currently, the integration diverges to infinity (or `NaN`) because the step-size adaptation logic is inverted—it increases the step size `dt` exponentially when it should be tightly controlled.

Your task is to:
1. Navigate to `/home/user/nanofit`.
2. Inspect and fix the `IntegrateODE` function in `ode.go`. Remove the faulty step-size adaptation and replace it with a constant step size of `0.001` to ensure stable, convergent Euler integration.
3. Run the scientific regression tests using `go test` in the `/home/user/nanofit` directory to verify your fix. All tests must pass.
4. Compile the software from source into an executable named `nanofit` inside the same directory.
5. Execute the compiled program to process the sequence data:
   `./nanofit --input /home/user/nanofit/data/signals.csv --output /home/user/results.csv`

The final output must be successfully written to `/home/user/results.csv`, and the source code must pass all regression tests.
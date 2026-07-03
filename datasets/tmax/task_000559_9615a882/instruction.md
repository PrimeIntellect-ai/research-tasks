You are an ML engineer preparing a synthetic orbital mechanics dataset to train a Physics-Informed Neural Network (PINN). You need to generate highly accurate trajectory data of a 2D two-body problem (a planet orbiting a star) using an adaptive step-size Runge-Kutta ODE solver.

The simulation code is located at `/home/user/simulator`. It imports a vendored numerical integration package located at `/app/vendor/go-rk45`.

Currently, there is a critical problem: when you run the simulator, the planetary orbits diverge wildly and the planet spirals outwards or inwards. This happens because the adaptive step-size logic in the vendored `go-rk45` package has a mathematical perturbation in its numerical stability calculation. Specifically, the error estimator used to adapt the step size `dt` computes the difference between the 4th and 5th order estimates incorrectly, causing the step size to grow unbounded or shrink inappropriately.

Your task:
1. Analyze the vendored package in `/app/vendor/go-rk45/integrator.go`. Locate the error estimation calculation for the adaptive step size (look for the difference computed between the two trajectory estimates). 
2. Fix the mathematical bug in the error calculation.
3. Re-run the simulation in `/home/user/simulator` to produce the dataset. The simulator is hardcoded to output a file at `/home/user/dataset.csv` containing columns for time, position, velocity, and total energy.
4. Verify that your dataset is numerically stable. The total energy (E) of the system should be conserved. 

The task will be evaluated programmatically by parsing `/home/user/dataset.csv` and computing the maximum relative energy drift `max(|E_t - E_0| / |E_0|)` over the entire simulation. To succeed, this metric must fall below a strict numerical threshold.
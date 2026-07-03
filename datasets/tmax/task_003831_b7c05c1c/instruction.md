You are a machine learning engineer preparing a dataset of ODE trajectories to train a Neural ODE. The data generation relies on a custom adaptive step-size ODE solver written in Go. 

However, the current solver (`/home/user/integrator.go`) diverges and fails with a `NaN` or `Inf` error when trying to solve a simple stiff differential equation:
`dy/dt = -15 * y`, with `y(0) = 1.0` from `t = 0` to `t = 2.0`.

Your task is to:
1. Identify and fix the bug in the step-size adaptation logic in `/home/user/integrator.go`. The step size should shrink when the estimated error is larger than the tolerance, but currently, it seems to grow.
2. Compile and run the corrected Go program. The program is already set up to output the integration steps to `/home/user/dataset.csv` in the format `t,y`.
3. After generating the CSV, use `gnuplot` (which is installed on the system) to generate a plot of the trajectory. Create a gnuplot script at `/home/user/plot.gp` that reads `dataset.csv` and outputs a PNG image to `/home/user/plot.png`. The plot should plot `y` versus `t` with lines.
4. Save the exact final computed value of `y` (the last row's `y` value in `dataset.csv`) into `/home/user/final_y.txt`.

Ensure all requested files (`dataset.csv`, `plot.gp`, `plot.png`, `final_y.txt`) exist in `/home/user/`.
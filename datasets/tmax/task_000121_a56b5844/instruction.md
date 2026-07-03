I am a researcher running Monte Carlo simulations of a newly discovered nonlinear dynamic system. Unfortunately, our simulation pipeline sometimes produces unphysical "glitch" trajectories alongside the valid ones. I need you to build a classifier in Go to automatically filter these out.

Write a Go program at `/home/user/classifier.go` and compile it to `/home/user/classifier`. 
Your program must take a single command-line argument: the path to a CSV file. The CSV files contain time-series data with three columns: `t`, `x`, `y` (with a header row).

Your program must determine if the trajectory is physically valid ("clean") or unphysical ("evil"). 
If the file is valid, print exactly "CLEAN" to standard output and exit with status code 0.
If the file is unphysical, print exactly "EVIL" to standard output and exit with status code 1.

A trajectory is considered physically valid if it satisfies BOTH of the following conditions:
1. **Kinematic consistency**: The variable `y` represents the time derivative of `x` (`dx/dt`). You must numerically integrate `y` over time `t` (using the trapezoidal rule). At any time step $i$, the absolute difference between the numerical integral $\int_{t_0}^{t_i} y(t) dt$ and the displacement $x(t_i) - x(t_0)$ must be strictly less than `0.05`.
2. **Conservation Law**: The system possesses a conserved nonlinear quantity $Q(x, y)$ which must remain constant throughout the trajectory. I have lost the exact analytical formula for $Q$, but I have provided a stripped black-box binary at `/app/q_oracle`. You can invoke it as `/app/q_oracle <x> <y>` (e.g., `/app/q_oracle 1.5 -0.2`) to compute $Q$ for any state. For a valid trajectory, the statistical variance of $Q$ across all points in the CSV must be less than `0.001`. Unphysical trajectories will exhibit a variance significantly higher than this.

You should test your logic. There are a few sample files in `/home/user/samples/` if you want to explore the data, but your solution must be robust enough to handle the hidden evaluation datasets.
You are a performance engineer analyzing a mysterious oscillating metric from a simulated distributed system. 

You have been given the source code for the simulator in `/home/user/sim_engine/sim.rs`.
Your objective is to:
1. **Compile and run the simulator from source.** It is a standalone Rust file. Compiling and running it will produce a file named `/home/user/trace.csv` containing two columns: time (`t`) and the metric (`y`).
2. **Write a new Rust program** at `/home/user/analyze.rs` to analyze this trace. Your program must NOT use any external crates (no `Cargo.toml`, standard library only) and must implement the following from scratch:
    * **Spectral Analysis:** Compute the Discrete Fourier Transform (DFT) to find the dominant integer frequency $f_{dom}$ of the signal in the range $1 \le f \le 10$ Hz.
    * **Numerical Integration:** Implement the Euler method to integrate the damped harmonic oscillator model:
      $dy/dt = v$
      $dv/dt = -k \cdot v - (2\pi f_{dom})^2 y$
      Use initial conditions $y(0) = 1.0, v(0) = 0.0$ and an integration time step of $\Delta t = 0.01$.
    * **MCMC Sampling:** Implement a Metropolis-Hastings Markov Chain Monte Carlo algorithm (using a simple custom PRNG like an LCG) to estimate the damping parameter $k$. 
      - Use a uniform prior for $k \in [0.1, 2.0]$.
      - Use a Gaussian likelihood function comparing your numerically integrated $y_{model}(t)$ against the $y$ values in `trace.csv` at the corresponding times. Assume a standard deviation $\sigma = 0.1$ for the likelihood.
      - Run the chain for at least 5000 iterations.
3. **Save the result:** Compute the mean of the posterior samples of $k$ (discarding the first 20% as burn-in) and save this value, rounded to exactly 1 decimal place (e.g., `1.2`), to the file `/home/user/k_estimate.txt`.

Ensure your analytical Rust program compiles with `rustc /home/user/analyze.rs` without requiring cargo or external dependencies.
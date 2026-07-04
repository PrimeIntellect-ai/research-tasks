You are a performance engineer tasked with profiling and fixing a scientific computing simulation. We have a Go-based application that simulates signal propagation across a molecular network using numerical integration.

The core simulation library is vendored at `/app/vendor/github.com/phys-sim/wavegraph`. Recently, the simulation has become extremely slow, timing out on larger networks. Initial profiling suggests the adaptive numerical integrator in this package is diverging or failing to adapt its step size correctly, effectively running at the minimum possible step size.

Your task has three parts:

1. **Fix the Vendored Package:**
   Inspect the source code of the vendored package at `/app/vendor/github.com/phys-sim/wavegraph` (specifically look at `integrator.go`). Find and fix the deliberate perturbation that is breaking the step-size adaptation logic. 

2. **Develop the Analysis Tool:**
   Write a Go program at `/home/user/analyze.go` that:
   - Initializes a simulation using the `wavegraph` package's `NewGraphSimulation(100)` function (which simulates 100 nodes).
   - Runs the simulation by calling `Run(10.0)` to simulate 10.0 seconds of time. This will return a `[]float64` slice representing the signal at the sink node.
   - Computes the discrete Fourier transform (FFT) amplitude spectrum of this signal.
   - Normalizes the amplitude spectrum so that it sums to 1.0 (treating it as a probability distribution).
   - Computes the Kullback-Leibler (KL) divergence between this normalized spectrum and a baseline distribution provided in `/home/user/baseline.json` (which contains an array of float64 values representing the baseline normalized spectrum).

3. **Output and Visualization:**
   - Your Go program must write the computed KL divergence as a single floating-point number to `/home/user/kl_divergence.txt`.
   - Your Go program must also generate a line plot comparing the simulated normalized spectrum and the baseline spectrum, saved to `/home/user/spectrum_plot.png`.

The automated verifier will build and run your `analyze.go` program. It will check if the simulation runs efficiently and if your computed KL divergence matches the expected mathematical result.
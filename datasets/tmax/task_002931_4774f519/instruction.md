You are acting as a systems engineer assisting a data scientist with a graph diffusion simulation written in Go. 

The data scientist is trying to fit a steady-state model to a specific network, but they are facing two distinct problems:
1. **Trapped Data:** The target graph parameters (edge weights) are only available in a scanned image located at `/app/network_params.png`. 
2. **Non-Reproducible Execution:** The current simulation code (`/home/user/sim/main.go`) uses concurrent goroutines to compute the next state. Because floating-point addition is not associative, the non-deterministic order of goroutine execution (and thus the order of accumulation into the state vector) causes the steady-state results to vary slightly across multiple runs. This breaks the automated testing pipeline.

Your objectives are:
1. **Extract Parameters:** Extract the directed edge weights from `/app/network_params.png`. The image contains text in the format `SourceNode -> DestNode : Weight`. (There are 4 nodes, labeled 0 through 3).
2. **Fix Reproducibility:** Refactor `/home/user/sim/main.go` so that the matrix-vector multiplication is strictly deterministic and reproducible, while maintaining the overall logic of the diffusion. You may remove the concurrency or implement a deterministic reduction strategy.
3. **Run the Simulation:** Update the hardcoded adjacency matrix in the Go code with the weights you extracted from the image. The initial state is a vector `[1.0, 0.0, 0.0, 0.0]`. Run the simulation for exactly 1000 iterations.
4. **Save the Results:** Output the final state vector (after 1000 iterations) to `/home/user/steady_state.txt`. The file should contain exactly 4 lines, each containing the floating-point value for nodes 0, 1, 2, and 3 respectively, formatted to at least 15 decimal places.

An automated verifier will run your compiled Go program multiple times to ensure the output is perfectly reproducible (variance = 0) and will evaluate your `steady_state.txt` against the exact analytical solution using a Mean Squared Error (MSE) metric. 

Ensure your final binary can be built inside the `/home/user/sim/` directory using standard `go build`. You may use tools like `tesseract` to read the image.
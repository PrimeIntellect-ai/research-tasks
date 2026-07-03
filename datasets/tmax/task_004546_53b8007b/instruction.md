You are a performance engineer tasked with debugging and deploying a Monte Carlo simulation pipeline for a high-frequency trading firm. The pipeline evaluates the pricing of a complex derivative, but currently suffers from non-reproducible results due to floating-point reduction order issues when running parallelized C code.

We have a legacy schematic provided as an image at `/app/schematic.png` which contains the initial parameters for the Monte Carlo simulation (a seed offset, a drift parameter, and a volatility parameter). 

Here are your tasks:
1. **Parameter Extraction**: Extract the three numerical parameters (Seed Offset, Drift, Volatility) from the image at `/app/schematic.png` using any OCR tool available to you (e.g., Tesseract).
2. **Simulation Fixing**: Write a C program `mc_sim.c` that runs a Monte Carlo simulation for 100,000 paths using the extracted parameters. The simulation must calculate the final asset price. The previous engineer used an unsafe parallel reduction that caused floating-point non-determinism. You must implement a strictly reproducible reduction method (e.g., Kahan summation or strict deterministic ordering) so the result is exactly reproducible across runs. 
3. **Curve Fitting/Optimization**: Run the deterministic simulation over 10 different starting prices (from 100 to 190 in steps of 10). Use these results to perform a basic linear regression (y = mx + c) where x is the starting price and y is the simulated final price.
4. **Service Deployment**: Create an HTTP server listening on `127.0.0.1:8080`. 
   - Endpoint `/simulate`: Accepts a GET request with a query parameter `start_price`. It should run the fixed C program (or use the pre-compiled binary) and return the exact deterministically computed final price as a plain text float.
   - Endpoint `/regression`: Accepts a GET request and returns the slope (`m`) and intercept (`c`) computed in step 3 as a JSON object: `{"slope": m, "intercept": c}`.
   - All endpoints must require a Bearer token in the Authorization header: `Bearer sim-perf-token-2024`.

Write the service in Python or C, but the core Monte Carlo logic *must* be executed via your fixed C program. Create a shell script `/home/user/start_service.sh` that compiles the C code and starts the web service.
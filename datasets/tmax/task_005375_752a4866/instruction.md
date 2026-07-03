You are a data scientist troubleshooting a distributed chemical kinetics modeling pipeline. We are attempting to fit models for a set of complex molecular reaction networks, but our numerical integration pipeline is failing.

We have a multi-service architecture located in `/home/user/app/`:
1. **Redis (Port 6379):** Holds observational data and network adjacency lists for the molecular graphs.
2. **Aggregator Service (Port 5000):** A Python Flask service that receives the integrated trajectories.
3. **Go Integrator Service (Port 8080):** A Go-based service that exposes an HTTP API. When triggered, it pulls the graph topology from Redis, formulates the non-linear ODEs for the system, solves them in parallel using goroutines, and pushes the reshaped data to the Aggregator.

**The Problem:**
When we trigger the Go integrator, the numerical solver diverges and outputs `NaN` values for certain stiff reaction networks. This is due to a faulty step-size adaptation mechanism in the Runge-Kutta solver located in `/home/user/app/integrator/solver.go`. The step-size `dt` is being scaled incorrectly when the local error exceeds the tolerance, causing it to overcompensate, drop to exactly `0.0`, and cause a divide-by-zero or infinite loop, rather than clamping to a minimum step size `min_dt = 1e-6`.

**Your Task:**
1. Fix the step-size adaptation logic in `/home/user/app/integrator/solver.go` so that `dt` never falls below `1e-6` and scales correctly using the standard RK4/5 error ratio formula (you'll see the `TODO` in the `adaptStep` function).
2. The Go service is missing its parallel computing setup. Modify the `ProcessNetworks` function in `/home/user/app/integrator/main.go` to process the equations using a WaitGroup and goroutines, allowing concurrent solving of the networks fetched from Redis.
3. Start the entire pipeline. The startup script `/home/user/app/start_services.sh` is provided, but you must ensure the Go integrator is compiled and running on `localhost:8080`.
4. The Go service must require an authorization header for its `/solve` endpoint: `Authorization: Bearer ds-model-fit-token`. Add this check to the HTTP handler. 
5. Write the final outputs of the fixed aggregator to `/home/user/results.log` by querying `http://localhost:5000/results` after triggering the Go service.

Trigger the pipeline using:
`curl -H "Authorization: Bearer ds-model-fit-token" -X POST http://localhost:8080/solve`

Ensure everything is running. The automated test will send its own complex graphs to your Go endpoint and check the resulting trajectories on the Aggregator service.
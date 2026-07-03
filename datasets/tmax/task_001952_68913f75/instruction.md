You are a data scientist working on fitting models for a complex chemical reaction network. We have a reference simulation engine provided as a stripped binary at `/app/chemical_oracle`. 

Your goal is to build a high-performance Go-based simulation API that replicates the physics of this oracle, but is optimized for large-scale model fitting. 

The chemical reaction network is described by the Robertson equations (a classic stiff ODE system):
dy₁/dt = -0.04 y₁ + 10⁴ y₂ y₃
dy₂/dt = 0.04 y₁ - 10⁴ y₂ y₃ - 3·10⁷ y₂²
dy₃/dt = 3·10⁷ y₂²

We attempted to implement an explicit Runge-Kutta solver in Go with step-size adaptation, but it diverges due to the extreme stiffness of the system. Your tasks are:

1. **Implement a Stiff ODE Solver**: Write a Go program that integrates this system using an implicit or semi-implicit method (e.g., Rosenbrock method or Backward Euler). You will need to implement the analytical Jacobian and use Matrix Decomposition (like LU decomposition) to solve the linear systems at each step.
2. **Expose an HTTP Service**: Your Go program must start an HTTP server listening on exactly `127.0.0.1:8080`.
3. **`/simulate` Endpoint**:
   - Method: `POST`
   - Content-Type: `application/json`
   - Request body: `{"y0": [y1, y2, y3], "t_end": 10.0}` (where `y0` is the initial state at t=0, and `t_end` is the integration time).
   - Response body: `{"y_final": [y1, y2, y3]}` (the state at `t_end`).
4. **Oracle Equivalence**: Your solver must return results that match the output of `/app/chemical_oracle` within a relative tolerance of `1e-4`. You can reverse-engineer or treat `/app/chemical_oracle` as a black box. It takes arguments: `/app/chemical_oracle <y1> <y2> <y3> <t_end>` and prints the final state as three space-separated floats.

Ensure your Go server runs indefinitely and correctly processes requests. The automated verifier will send HTTP POST requests to your service to test for accuracy against the oracle across various integration times and initial states.
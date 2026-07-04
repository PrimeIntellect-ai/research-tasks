I am a data scientist working on fitting some physical models, and I've reduced the core problem to solving a specific nonlinear equation for a series of datasets. I need to orchestrate this using a simple bash-based workflow that mimics a notebook execution, running a highly parallelized Rust program.

The nonlinear equation to solve for $x$ is:
$f(x) = x^3 - \cos(x) - c = 0$

I have a JSON file acting as my "notebook" of experiments at `/home/user/workflow.json` with the following format:
```json
{
  "experiments": [
    {"id": "exp1", "c": 1.0},
    {"id": "exp2", "c": 2.0},
    {"id": "exp3", "c": 5.0},
    {"id": "exp4", "c": 10.0}
  ]
}
```

Please do the following:
1. Initialize a Rust project at `/home/user/solver`.
2. Write a Rust program in this project that reads `/home/user/workflow.json`.
3. Use the `rayon` crate to parallelize the solving process across the experiments.
4. For each experiment, solve the nonlinear equation for $x$ (assume $x > 0$) using a method like Newton-Raphson or Bisection, achieving a precision of at least $10^{-5}$.
5. Output the results to `/home/user/results.json` in this exact format:
```json
{
  "exp1": 1.12842,
  "exp2": 1.38523
}
```
*(Values above are illustrative, compute the actual roots).*
6. Create a bash orchestration script at `/home/user/run_workflow.sh` that, when executed, builds the Rust project in release mode and runs it to produce `/home/user/results.json`. Ensure the script is executable.

The test will simply call `/home/user/run_workflow.sh` and then verify the contents of `/home/user/results.json`.
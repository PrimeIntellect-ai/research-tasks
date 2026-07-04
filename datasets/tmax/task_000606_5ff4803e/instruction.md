You are a performance engineer profiling a newly developed distributed N-body physics simulation. Recently, several simulation nodes have crashed due to numerical divergence. You suspect the adaptive step-size controller is failing to correctly reduce the integration step size when the energy error spikes.

The simulation generates log files in the directory `/home/user/sim_logs/`. Each file is named `node_XX.log` (e.g., `node_01.log`).
The logs contain space-separated values with the following columns:
`Iteration StepSize EnergyError`

According to the analytical design of the integrator, the step-size adaptation must strictly obey the following rule:
**If the `EnergyError` at iteration $i$ is strictly greater than `0.005`, the `StepSize` at iteration $i+1$ MUST be less than or equal to $0.5 \times$ the `StepSize` at iteration $i$.**

Your task is to write a Bash script at `/home/user/audit_sim.sh` that processes all log files in `/home/user/sim_logs/` and validates this analytical rule (comparing the observed reshaping of the step size against the expected theoretical bound). 

1. Your script must find all rule violations across all nodes. A violation occurs when `EnergyError` at iteration $i$ > 0.005, but `StepSize` at $i+1$ is > 0.5 * `StepSize` at $i$.
2. Tally the total number of violations for each node.
3. Generate a JSON report at `/home/user/report.json`. The JSON should be a single dictionary mapping the node name (e.g., "node_02") to its integer violation count. 
4. **Only include nodes in the JSON report that have 1 or more violations.**
5. Format the JSON nicely (e.g., using `jq`).

Example expected output format for `/home/user/report.json`:
```json
{
  "node_02": 4,
  "node_04": 7
}
```

Constraints:
- Use pure Bash and standard Unix tools (`awk`, `sed`, `bc`, `jq`, etc.) to perform the data processing.
- Make sure `/home/user/audit_sim.sh` is executable and runs without user input.
- Run your script to generate `/home/user/report.json` before concluding.
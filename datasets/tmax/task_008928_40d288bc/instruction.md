You are a network engineer assisting with a failing local CI/CD pipeline for a new Go-based data ingestion system. 

The pipeline runs in an environment with strict simulated disk quotas. Currently, the CI pipeline is failing due to two issues: a connectivity misconfiguration between the microservices and a storage quota violation.

Here is the setup located in `/home/user/ci_pipeline/`:
- `run.sh`: The main CI script that builds the services, starts the storage monitor, starts the processor, and runs the collector.
- `processor/main.go`: A Go service that listens for TCP connections and writes incoming data to `/home/user/ci_pipeline/data/store.log`.
- `collector/main.go`: A Go service that connects to the processor and sends 20MB of simulated log data.
- `monitor/main.go`: A background service started by the CI script that continuously monitors the `/home/user/ci_pipeline/data/` directory. If the directory size exceeds 10MB, it kills the pipeline to simulate a disk quota limit.

Your tasks:
1. **Connectivity Diagnostics**: The `collector` is currently failing to reach the `processor`. Identify the network misconfiguration in the Go source code and fix it so the collector successfully connects to the processor's actual listening port.
2. **Storage Quota Management**: The collector sends 20MB of data, but the pipeline has a strict 10MB storage limit enforced by the monitor. Modify `processor/main.go` so that instead of writing the entire raw payload to disk, it reads and discards the incoming data, and writes ONLY the exact string `PROCESSED SUCCESS` to `/home/user/ci_pipeline/data/store.log`.
3. **Pipeline Execution**: Execute the CI pipeline by running `/home/user/ci_pipeline/run.sh`. 

The task is successfully complete when the pipeline finishes without being killed by the monitor, and the CI script automatically generates the artifact file at `/home/user/ci_pipeline/artifacts/pass.txt`.
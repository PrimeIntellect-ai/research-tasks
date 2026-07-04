We have a failing build in our log processing pipeline. Our pipeline uses a bash script to sanitize logs before they reach the consumer, but a recent commit introduced a regression, and the services are currently disconnected.

Your goals are to diagnose the regression, fix the sanitization script, and reconnect the pipeline.

1. **Find and Fix the Regression**: 
   A bash script at `/app/repo/filter.sh` reads log lines from `stdin` and writes valid ones to `stdout`. 
   Valid logs must match the exact format: `YYYY-MM-DD HH:MM:SS [LEVEL] Metric=<number>`
   - `LEVEL` must be exactly one of: `INFO`, `WARN`, `ERROR`
   - `<number>` must be an integer where `0 <= number <= 100`.
   
   A recent commit in `/app/repo` broke the boundary logic for the metric (it now rejects legitimate edge values like 0 and 100). Use git bisection or manual inspection to find the bug, fix `/app/repo/filter.sh`, and copy the fully working version to `/home/user/final_filter.sh`.

2. **Reconnect the Services**:
   The environment has a startup script `/app/start_services.sh` running two background services:
   - **Log Emitter:** Listens on `localhost:8001` and streams raw logs.
   - **Log Consumer:** Listens on `localhost:8002` and expects sanitized logs.
   
   Use bash networking tools (like `nc` or bash's `/dev/tcp`) to continuously read from the emitter on port 8001, pipe the output through your fixed `/home/user/final_filter.sh`, and send the results to the consumer on port 8002. Leave this pipeline running in the background.

Ensure `/home/user/final_filter.sh` is perfectly robust. It will be aggressively tested against a suite of clean and malformed log lines.
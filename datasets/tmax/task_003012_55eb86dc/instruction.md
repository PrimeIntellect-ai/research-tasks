I am reviewing a broken PR for our internal numerical expression evaluator service. The PR author updated the project to use Go concurrency patterns (goroutines and channels) to evaluate numerical algorithms in parallel, but the CI is failing. 

The source code for the service is vendored at `/app/go-numcalc-v1.2.3`. 

Here is what you need to do:
1. The PR author completely broke the Bash build and startup scripts. `build.sh` has bash syntax errors and incorrect environment variable assignments that prevent compilation. `run.sh` is supposed to start the compiled binary but fails to pass the required authentication token. Fix both `/app/go-numcalc-v1.2.3/build.sh` and `/app/go-numcalc-v1.2.3/run.sh`.
2. Ensure the service compiles successfully into a binary named `numcalc` in the same directory.
3. Start the service using your fixed `run.sh`. The service must be left running in the background.

The service must run on `localhost` and bind to:
- **Port 8081 (HTTP)**: A health check endpoint at `/health`
- **Port 8080 (TCP)**: A custom line-based expression emulator protocol. 

The service requires the environment variable `AUTH_TOKEN` to be set to `calc_secure_99` in order to accept TCP connections, which you must properly export in `run.sh`.

Please fix the scripts, build the service, and leave it running. I will run an automated verification suite against the ports to ensure the PR is fixed.
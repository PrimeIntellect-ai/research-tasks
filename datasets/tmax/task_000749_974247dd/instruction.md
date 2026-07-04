**Ticket #9942: Fraud Detection Pipeline Down & Calculation Errors**

Hello IT Support,

We are experiencing a major outage and data accuracy issue with our Fraud Detection pipeline. The system is composed of four services:
1. An `nginx` reverse proxy serving the API on port 8080.
2. A `flask` API gateway query router.
3. A `redis` instance for caching intermediate states.
4. A custom C backend (`fraud_aggregator`) that calculates the rolling average and peak transaction values from raw binary logs.

**Issue 1: Pipeline is completely down**
Requests to `curl http://localhost:8080/api/fraud_status` are returning 502 Bad Gateway. The startup script `/home/user/app/start_services.sh` brings up all services, but they seem to be misconfigured and cannot communicate with each other. Please trace the state across the services, fix their configuration files located in `/home/user/app/config/`, and restart them so the pipeline functions end-to-end.

**Issue 2: Algorithmic calculation bug**
Before the outage, the customer service team reported that the rolling peak calculations were wrong. We suspect a bug in the C codebase (`/home/user/app/src/fraud_aggregator.c`). The C program reads a stream of 32-bit integers (transactions) from stdin and outputs a formatted summary to stdout. 
Compare its output against the legacy reliable binary provided at `/home/user/app/legacy/oracle_aggregator` to debug the query results. 

**Your Tasks:**
1. Fix the configurations in `/home/user/app/config/` (nginx.conf, flask_app.py, backend.conf) to restore the flow: Nginx -> Flask -> C Backend -> Redis.
2. Debug and fix the C source code in `/home/user/app/src/fraud_aggregator.c`. 
3. Recompile the fixed C code to `/home/user/app/bin/fraud_aggregator`.
4. Leave the services running with the correct configuration.

Please resolve this ticket ASAP.
You are assisting a network engineer who is troubleshooting and repairing a broken email relay pipeline. We have a set of containerized-style services running locally for testing, but the core security policy filter has been lost, causing connectivity and mail delivery to fail.

Your task has three parts:

**Part 1: Implement the Security Filter**
You need to write a Python script at `/home/user/sanitize.py` that acts as the core filtering logic. It must read a raw email payload from `stdin` and print the sanitized version to `stdout`. 
The rules for sanitization are strict. You must apply them exactly as follows, in this order:
1. Remove any line starting exactly with `X-Internal-Trace-ID: ` (including the space).
2. Insert a new header `X-Processed-By: SecRelay-v1` immediately after the `Subject: ` line. If there is no `Subject: ` line, append it to the very beginning of the input (as the first line).
3. Replace all occurrences of the exact substring `http://insecure.local/` with `https://secure.local/` anywhere in the body or headers.
4. Normalize line endings to standard Unix `\n` (if any Windows `\r\n` are present, convert them).

**Part 2: Multi-Service Composition & Routing**
There are two mock container services provided in `/app/`:
- The Ingress Mail Service (simulating incoming network traffic).
- The Egress Mail Service (simulating the outbound delivery queue).

Currently, the Ingress service is trying to forward payloads to a local port `10026`, but nothing is listening. The Egress service listens on port `10027`. 
You must write a daemonization script, `/home/user/relay_daemon.sh`, that listens on TCP port `10026`. When a connection is received, it must read the payload, pass it through your `/home/user/sanitize.py` script, and immediately forward the resulting output to TCP port `10027` (the Egress service). You may use `socat`, `nc`, or Python for this routing daemon.

**Part 3: Idempotent Lifecycle Configuration**
Write a bash script `/home/user/setup_env.sh` that:
1. Starts the background mock services by executing `/app/start_services.sh`.
2. Idempotently starts your `relay_daemon.sh` in the background (i.e., if it's already running, it restarts it or leaves it running, ensuring port 10026 is bound to your logic).
3. Validates the flow by echoing a test string containing `Subject: Test` and `http://insecure.local/` to `localhost:10025` (where the Ingress service listens).

Ensure all scripts are executable. Your `sanitize.py` must be completely deterministic and flawlessly implement the text transformations, as it will be rigorously tested against an oracle with randomized inputs.
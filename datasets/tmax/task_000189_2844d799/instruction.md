You are an SRE responding to an urgent incident regarding our uptime monitoring aggregation service. The service is reporting incorrect, mathematically impossible exponential moving averages (EMA) for uptime, and the counters occasionally drop requests under load due to an alleged race condition.

Here is what you need to do to resolve the incident:

1. **Identify the affected Tenant:** The on-call engineer left an audio note before their shift ended at `/app/incident_voicemail.wav`. Transcribe it to find the specific `tenant_id` that is causing the alert.
2. **Recover Authentication:** The service requires an API key to initialize, which was accidentally committed to the Git repository in `/app/uptime_repo` and subsequently removed. You need to perform Git forensics to find the `X-API-Key` secret in the commit history.
3. **Fix the Mathematical Query Bug:** The `calculate_ema` function in `/app/uptime_repo/server.py` is miscalculating the moving average. Review the mathematical formula used for the EMA and fix it. The correct formula for an EMA given a new value $V$, previous EMA $S$, and smoothing factor $\alpha$ is: $S_{new} = \alpha \times V + (1 - \alpha) \times S$.
4. **Fix the Concurrency Bug:** The async endpoint `/record_ping/{tenant_id}` in `/app/uptime_repo/server.py` reads a metric, performs an async database mock sleep, and then writes the updated metric. Under concurrent load, this causes a race condition (lost updates). Fix the code to be thread/async-safe (e.g., using `asyncio.Lock`).
5. **Run the Service:** Start the fixed service so it listens continuously on `127.0.0.1:9090`. 

The automated verifier will act as a client, sending simulated concurrent pings to the service using the recovered API key in the `X-API-Key` header, and then it will query the mathematical EMA for the tenant ID mentioned in the audio file to ensure it matches the mathematically correct value.
You are an operations engineer triaging an incident. Our backend math worker service crashed recently. We suspect the crash was caused by a numerical instability issue in the standard deviation calculation leading to a `ValueError: math domain error`, but we don't know which request caused it.

You have been provided with the following files:
1. `/home/user/calc_stddev.py`: The exact script used by the math worker to calculate standard deviation. It takes a JSON payload string as a command-line argument.
2. `/home/user/worker_mem.dump`: A raw memory dump of the crashed worker process. The incoming JSON payloads (containing a `req_id` and a `data` array of floats) were kept in memory right before the crash.
3. `/home/user/api.log`: The frontend API logs, which record the timestamps and request IDs of all incoming jobs.

Your task:
1. Analyze the memory dump to extract the recent JSON payloads processed by the worker.
2. Fuzz/test the `calc_stddev.py` script using these extracted payloads to identify exactly which data array triggers the numerical instability crash.
3. Once you identify the crashing payload, cross-reference it with the `api.log` to reconstruct the timeline and find the exact timestamp of the failed request.
4. Write your final findings to `/home/user/triage_result.txt` in the following format exactly:
```
ReqID: <the-request-id>
Timestamp: <the-timestamp>
```
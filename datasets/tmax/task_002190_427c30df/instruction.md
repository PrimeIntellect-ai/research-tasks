You are an operations engineer triaging an incident involving a stalled distributed tracing system. 

Our custom log aggregation script, located at `/home/user/log_aggregator.py`, is supposed to reconstruct the timeline of events for a given transaction by following an event chain across multiple microservices. However, the script is currently failing to complete successfully.

When we run it, we encounter two main issues:
1. It sometimes hangs forever or crashes due to infinite loops.
2. It throws an `AssertionError` regarding the chronological ordering of timestamps, which prevents the timeline from being generated.

Your task is to debug and fix `/home/user/log_aggregator.py` so that it successfully processes the event chain starting from `evt-start`. 

Requirements:
1. Fix the infinite loop issue. Log chains can sometimes contain circular references due to a known retry-logic bug in our messaging queue. Your script must detect if an event ID has already been processed and terminate the loop cleanly without throwing an error, keeping the events processed up to that point.
2. Fix the assertion failure. The script enforces that timestamps strictly increase or remain the same. However, one of our legacy services logs its Unix timestamps in milliseconds, while the rest log in seconds. You need to normalize any millisecond-scale timestamps (those greater than `1e11`) to seconds (as floats or integers) *before* the assertion check and *update the event dictionary* with the normalized timestamp.
3. Once the script is fixed, run it to generate the final output.
4. The script should write the successfully reconstructed timeline as a JSON array to `/home/user/timeline_TXN-999.json`.

Do not modify the underlying JSON log files in `/home/user/logs/`. Only modify `/home/user/log_aggregator.py`.
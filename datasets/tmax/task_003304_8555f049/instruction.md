You are an SRE on a platform reliability team. We have a Python script, `/home/user/fast_sla_calc.py`, designed to rapidly compute global uptime metrics from high-volume, multithreaded log streams. Unfortunately, the script has a few critical bugs:

1. **Concurrency/Deadlocks:** It uses multithreading to aggregate downtime metrics from different regions, but under high contention, the thread synchronization causes deadlocks. 
2. **Floating-point Precision Repair:** The script naively accumulates millions of microsecond-level downtime intervals using standard float addition. This causes catastrophic cancellation and precision loss compared to our legacy SLA calculator. You must repair this to ensure mathematically exact accumulation.
3. **Format Parsing Edge-cases:** The incoming log streams sometimes represent small downtime durations in inconsistent formats (e.g., `"1.5e-4"`, `"<0.001"`, or strings with trailing `"ms"`). The script currently crashes or silently truncates these.

Furthermore, the regional weighting used in the calculation must be strictly updated. The previous SRE lead uploaded a screenshot of the new SLA weighting formula to `/app/sla_weights.png`. You must extract the exact float weights from this image and update them in the script.

**Your Task:**
1. Read `/app/sla_weights.png` to recover the 3 regional weights (us-east, eu-west, ap-south).
2. Debug and rewrite `/home/user/fast_sla_calc.py` so that it safely handles concurrent input without deadlocking.
3. Implement robust float parsing for the duration fields and use precision-safe math (e.g., Kahan summation, or Python's built-in robust summation features) to accumulate the downtimes.
4. The script must read a JSON array of events from `stdin`. Each event is a dictionary: `{"region": "us-east", "downtime": "0.0012ms"}`.
5. The script must output a single floating-point number to `stdout` representing the total weighted downtime across all regions, formatted to exactly 8 decimal places.

An automated fuzzer will run your script against thousands of test cases and compare its standard output exactly against a reference oracle. You must fix all deadlocks, parsing errors, and precision drops to pass.
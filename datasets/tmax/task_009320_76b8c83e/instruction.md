You are a Site Reliability Engineer (SRE) responsible for monitoring uptime and calculating Service Level Agreement (SLA) penalties for recent service incidents. 

You have been provided with a local SQLite database containing the incident logs at `/home/user/uptime.db` and a Python script at `/home/user/calculate_sla.py` which computes the compounding SLA penalties.

Currently, the script is broken. When run, it crashes due to a combination of data anomalies triggering internal assertions, and a mathematical function hitting maximum recursion depth limits.

Your task:
1. Debug and fix the SQL query in `/home/user/calculate_sla.py` to appropriately filter out invalid records. Specifically, the query should ONLY return incidents where the `end_time` is strictly greater than or equal to the `start_time`, and it must EXCLUDE any maintenance windows (maintenance windows are indicated by a `severity` of 0).
2. Debug and fix the `compute_cascade_penalty` recursive function in the script. The function is supposed to compound the penalty by adding a base severity score for every 60-minute chunk (or partial chunk) of downtime. However, it currently enters infinite recursion for most inputs. Fix the loop/recursion termination condition so it properly halts and calculates the correct mathematical penalty.
3. Once the script is fixed, run it. If successful, all intermediate assertion-based validations will pass, and the script will calculate a final integer SLA penalty score.
4. The script is already configured to write its final output to `/home/user/sla_penalty_result.txt`. Ensure this file is generated successfully and contains only the final integer score.

Do not change the penalty calculation formula (severity * 10 added per 60-minute chunk or partial chunk), only fix the bugs causing the crash.
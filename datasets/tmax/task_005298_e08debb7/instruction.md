You are acting as a systems compliance officer conducting an audit of internal data access logs. We need to detect a specific anomalous pattern: "repeated unauthorized access attempts across the organizational hierarchy." 

You must write a C program that analyzes a stream of access logs and identifies users violating compliance rules.

Our environment has two services you need to interact with:
1. **Directory Service (Redis)**: Running on `127.0.0.1:6379`. It stores two types of string keys:
   - `mgr:<user_id>` -> The user ID of their direct manager. (The CEO has no manager).
   - `owner:<resource_id>` -> The user ID of the employee who owns the resource.
2. **Log API (HTTP)**: Running on `127.0.0.1:8080`. An endpoint `GET /logs` streams 200,000 plain-text CSV access logs in the format: `timestamp,user_id,resource_id`. (Timestamps are UNIX epoch integers, sorted chronologically).

### Compliance Rules
1. **Access Legality**: An access event by `user_id` on `resource_id` is considered "Unauthorized" IF:
   - The `user_id` is NOT the owner of the resource.
   - AND the `user_id` is NOT in the direct upward management chain of the resource owner (i.e., you must recursively resolve `mgr:` keys starting from the resource owner to check if `user_id` is one of their managers/directors/VPs).
2. **Window Function Aggregation**: We only formally flag a user for audit if they accumulate **3 or more Unauthorized Accesses within any rolling 60-second window**.

### Your Task
1. There is a startup script `/app/start_services.sh` which launches Redis and the Log API. Run it.
2. Write a C program at `/home/user/audit.c` to perform this compliance audit. 
3. You may use standard libraries and `hiredis` or `libcurl` if you wish, or just execute shell commands like `curl` and `redis-cli` from within C using `popen`. 
4. The C program must output the list of flagged users and the exact timestamp that triggered the 3rd unauthorized access in a window. Write this to `/home/user/flagged.csv` in the format: `user_id,trigger_timestamp`. (If a user triggers multiple separate windows, list all trigger timestamps for them).
5. Compile your C program to `/home/user/audit` and run it.

We will grade your `/home/user/flagged.csv` against a hidden ground-truth file using an F1-score metric.
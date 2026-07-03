You are a DevOps engineer responding to a system incident. A critical log aggregation script has failed, and one of the source log files was accidentally deleted during a faulty rotation. 

Your objective is to recover the deleted data, fix the bash-based aggregation script, and produce a correctly ordered timeline of events.

**Phase 1: Deleted File Recovery**
The logs for Service C were written to `/home/user/logs/service_c.log`, but the file was accidentally deleted. Fortunately, a background process named `service_c_emitter` is still running and holds the file open.
1. Inspect the running processes and recover the deleted file contents.
2. Save the recovered contents to `/home/user/logs/service_c_recovered.log`.

**Phase 2: Fix the Aggregation Script**
We have three log files:
- `/home/user/logs/service_a.log` (Format: `YYYY-MM-DDTHH:MM:SSZ MESSAGE`) -> Timestamps are in UTC.
- `/home/user/logs/service_b.log` (Format: `YYYY-MM-DD HH:MM:SS-TZ MESSAGE`) -> Timestamps are in a specific timezone offset (e.g., -04:00).
- `/home/user/logs/service_c_recovered.log` (Format: `EPOCH MESSAGE`) -> Timestamps are in Unix Epoch.

The script `/home/user/scripts/aggregate.sh` attempts to combine these files into a unified timeline but fails a convergence check because it uses naive alphabetical sorting, mixing up timezones and formats. 
1. Modify `/home/user/scripts/aggregate.sh` to properly parse the different time formats.
2. Convert all timestamps to Unix Epoch.
3. Output the combined logs sorted chronologically (oldest to newest) to `/home/user/logs/unified.log`.
4. The final `/home/user/logs/unified.log` must have the exact format: `[EPOCH] [SERVICE_NAME] [MESSAGE]`. (Where SERVICE_NAME is `ServiceA`, `ServiceB`, or `ServiceC`).

**Constraints:**
- You must use Bash and standard Linux tools (e.g., `awk`, `sed`, `date`, `sort`). Python, Perl, or other interpreters are not allowed.
- The `aggregate.sh` script currently exists but is buggy. You may rewrite it completely as long as it executes successfully and generates the final output.
- Do not stop the `service_c_emitter` process.

Ensure the final log file is written exactly to `/home/user/logs/unified.log`.
You are a cloud architect migrating a legacy backend for our log analysis platform. As part of this migration, we have containerized a legacy log processor, but we discovered it is fragile and vulnerable to specific malformed log entries.

Your objectives are as follows:

1. **Analyze the Legacy Binary:** 
   There is a stripped binary located at `/app/legacy_parser`. It reads log lines from standard input and processes them. However, it crashes or behaves maliciously when fed certain inputs. You need to analyze this binary (or observe its behavior) to deduce the exact conditions that cause it to fail.

2. **Implement a Sanitiser:**
   Write a Python script at `/home/user/sanitiser.py`. This script must act as a standard Unix filter: reading log lines from `stdin` and printing them to `stdout`. 
   - If a line is safe, print it exactly as received.
   - If a line triggers the vulnerabilities in `/app/legacy_parser`, silently drop it (do not print it).
   
   To help you develop your logic, we have provided sample log files in `/app/corpora/clean/` (which must be preserved entirely) and `/app/corpora/evil/` (which must be completely filtered out). Your final script will be rigorously tested against an expanded, hidden adversarial corpus.

3. **Fix the Systemd Deployment:**
   We run this pipeline via user-level systemd services. There is a service configured at `/home/user/.config/systemd/user/log-pipeline.service` which pulls logs via an SSH tunnel (managed by `tunnel.service`) and pipes them into the legacy parser.
   Currently, `log-pipeline.service` fails to start reliably on boot because of a missing dependency—it attempts to start before the tunnel is established. Fix the configuration file so that it strictly waits for `tunnel.service` to start.
   Additionally, modify its `ExecStart` line to insert your `/home/user/sanitiser.py` into the pipeline right before `/app/legacy_parser`.

Ensure your Python script is executable and robust. Do not modify the legacy binary or the corpora files.
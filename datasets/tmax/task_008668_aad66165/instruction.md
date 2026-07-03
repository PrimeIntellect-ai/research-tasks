You are an IT support technician responding to an urgent ticket (Ticket #4099). A data ingestion pipeline has broken down due to two issues in the `/home/user/ticket_4099` repository.

First, the downstream API requests are failing because the API key was recently revoked, but the new token is missing. The original developer claims they accidentally hardcoded the backup API token in the script, committed it, and then removed it in a subsequent commit to hide their mistake.

Second, the main parsing script (`/home/user/ticket_4099/parser.py`) is hanging indefinitely in production. It processes log strings, but encounters an infinite loop when given malformed logs containing unclosed brackets.

Your tasks are:
1. **Secret Recovery:** Forensically examine the git history of the `/home/user/ticket_4099` repository to find the removed backup API token (it was assigned to a variable named `BACKUP_API_SECRET`). Extract the exact token string and write it to `/home/user/secret.txt`.
2. **Loop Termination Fix:** Inspect the `extract_tags(log_string)` function in `/home/user/ticket_4099/parser.py`. It currently enters an infinite loop if a log string contains a `[` without a corresponding `]`. Fix the function so that if it encounters an unclosed bracket (i.e., missing `]`), it immediately raises a `ValueError("Malformed input")` instead of looping indefinitely. The function must still correctly extract tags for well-formed inputs (e.g., `"[ERROR] User login"` should return `["ERROR"]`).

Ensure that your fixed script correctly handles both valid and malformed inputs. The automated test will verify the contents of `/home/user/secret.txt` and run unit tests against your fixed `parser.py` script.
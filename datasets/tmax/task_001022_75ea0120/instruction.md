You are an operations engineer triaging an ongoing incident. A Python background worker process has been experiencing intermittent failures in production. You have been provided with an archive of the container logs and the application source code.

Your objectives are to:
1. **Analyze the Logs**: Inspect `/home/user/incident_triage/container_logs.log` to identify the failing jobs. The logs contain a mix of INFO logs (which include the job IDs and incoming JSON payloads) and ERROR logs (which indicate when a job failed).
2. **Reproduce the Failure**: Correlate the ERROR logs with the preceding INFO logs to extract the exact JSON payload that triggers the intermittent crash. Save this exact JSON payload into a file at `/home/user/incident_triage/repro_payload.json`.
3. **Resolve the Dependency Conflict**: The application depends on packages listed in `/home/user/incident_triage/requirements.txt`. The intermittent crash is caused by a dependency conflict that is only triggered when specific conditional logic (driven by the payload) is executed. 
   Create a new Python virtual environment at `/home/user/triage_venv`. Install the requirements, but you must identify and apply the correct version constraints to resolve the crashing issue without modifying the application code. Note: Due to strict legacy compatibility requirements in the wider system, `Jinja2` MUST remain at version `2.11.3`.
4. **Verify**: Prove the fix works by running `/home/user/incident_triage/processor.py` with your extracted payload using the Python executable from your fixed virtual environment.
5. **Report**: Create a file at `/home/user/incident_triage/resolution.txt` containing the name and exact pinned version of the secondary dependency you had to downgrade to resolve the conflict (e.g., `SomePackage==1.2.3`).

Do not modify `processor.py` or `notifier.py`. Your fix must be purely at the dependency level.
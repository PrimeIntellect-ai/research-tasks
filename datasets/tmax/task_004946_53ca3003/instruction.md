[URGENT] 3AM PAGE - PagerDuty Alert #9942
Priority: P0
Service: Forensic-Log-Ingestion

Wake up. Our forensic automated ingestion pipeline has collapsed under a targeted payload attack. The anomaly detection service is stuck in an infinite loop due to a convergence failure in the baseline mathematical solver, and malicious payloads are slipping into the data lake.

Before his phone battery died, the primary on-call engineer left a voicemail at `/app/voicemail.wav`. You need to transcribe this audio to get the correct algorithmic constants and formula corrections required to fix the convergence failure in `/home/user/anomaly_solver.py`.

Your objectives:
1. Fix the convergence failure in `/home/user/anomaly_solver.py` using the instructions hidden in the audio voicemail. The solver currently uses an iterative method that diverges because the decay constant and denominator are incorrect. Use an interactive debugger or print statements to trace the state if necessary.
2. Build a Python-based sanitizer at `/home/user/classifier.py`. We have isolated a corpus of known adversarial log payloads that triggered the incident, as well as safe logs.
   - The classifier must take a single file path as a CLI argument: `python3 /home/user/classifier.py <path_to_log>`
   - It must exit with code `0` if the log is clean/safe.
   - It must exit with code `1` if the log is malicious/adversarial.
3. The adversarial logs exploit a specific parsing vulnerability involving recursive shell-escapes hidden within Base64-encoded JSON values. Your classifier must decode the payload and flag any entries containing more than 3 layers of nested encoding.

Write your final regression test results to `/home/user/incident_report.log` containing a single line with the fixed decay constant value used in the solver.
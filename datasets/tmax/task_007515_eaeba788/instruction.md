As an incident responder, you are investigating a system compromise where an application trace log accidentally recorded sensitive user credentials. To safely share these logs with the wider team without leaking data, you must write a secure Rust utility to sanitize the log file. 

The original sensitive log is located at `/home/user/incident_logs/app_trace.log`.

Your task is to:
1. Initialize a new Rust executable project at `/home/user/redactor`.
2. Write a Rust program in this project that reads `/home/user/incident_logs/app_trace.log`.
3. The program must redact sensitive data by applying the following rules:
   - Any 16-character alphanumeric session token following `SESSION_TOKEN=` must be replaced such that the output reads `SESSION_TOKEN=[REDACTED]`.
   - Any non-whitespace string of characters following `PASSWORD=` must be replaced such that the output reads `PASSWORD=[REDACTED]`.
4. The program must write the sanitized logs to `/home/user/incident_logs/app_trace_safe.log`.
5. To enforce strict access control, your Rust program must set the file permissions of the newly created `app_trace_safe.log` to exactly `0400` (read-only for the owner) immediately after writing to it.

Once your Rust program is complete, build and run it so that the `/home/user/incident_logs/app_trace_safe.log` file is successfully generated with the correct redactions and permissions.
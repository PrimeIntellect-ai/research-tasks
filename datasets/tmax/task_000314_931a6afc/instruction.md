You are a support engineer investigating a bug in a distributed Rust application. A customer reported that their specific request, `REQ-008`, failed. 

You have been provided with the following files in the system:
- Source code for the frontend service: `/home/user/app/frontend/src/main.rs`
- Source code for the backend service: `/home/user/app/backend/src/main.rs`
- Configuration file used in production: `/home/user/app/.env`
- Logs from the incident: `/home/user/logs/frontend.log` and `/home/user/logs/backend.log`

Your tasks are:
1. **Fix the Environment Misconfiguration**: The system has been failing due to a misconfigured environment variable in `/home/user/app/.env`. By reading the Rust source code for both services, identify which environment variable is incorrectly named or has an invalid unit/value that would cause a timeout or connection failure, and update the `/home/user/app/.env` file with the correct key and/or value.
2. **Reconstruct the Timeline**: Write a Rust program. You may initialize a new cargo project at `/home/user/tools/log_analyzer`. Your Rust program must read both `/home/user/logs/frontend.log` and `/home/user/logs/backend.log`, extract all log lines associated with request ID `REQ-008`, parse their timestamps, and sort them in chronological order.
3. **Generate a Diagnostic Report**: Your Rust program must output a JSON file at `/home/user/diagnostic_report.json` with the following structure:
```json
{
  "misconfigured_key": "<The exact environment variable name that was wrong in .env>",
  "corrected_value": "<The corrected value you put in .env>",
  "timeline": [
    {
      "service": "<'frontend' or 'backend'>",
      "timestamp": "<The exact timestamp from the log>",
      "message": "<The rest of the log message after the request ID>"
    }
  ]
}
```

Requirements:
- The `timestamp` should be extracted as-is from the log file, but sorting must be done chronologically.
- Log lines in the provided files follow the format: `[YYYY-MM-DDTHH:MM:SS.mmmZ] INFO [REQ-XXX] <message>`
- The `message` field in your JSON should be exactly the text that follows the `[REQ-XXX] ` part, stripped of leading/trailing whitespace.
- Run your Rust program to generate the `/home/user/diagnostic_report.json` file.
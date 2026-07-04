You are a Site Reliability Engineer (SRE) investigating an intermittent uptime issue in a microservices payment pipeline. Customers are occasionally reporting that their payments fail, but the issue is hard to pin down because it happens rarely and the errors span multiple services.

You have been provided with logs from the three services involved in the transaction pipeline: the API Gateway, the Auth Service, and the Payment Backend. The logs have been collected and placed in `/home/user/logs/`.

Your objective is to reconstruct the timeline of requests across these services, trace the intermediate state of the payment retries, and identify the exact requests that failed due to this intermittent issue.

### Service Log Formats

1. **API Gateway** (`/home/user/logs/api_gateway.log`)
   - Format: `[YYYY-MM-DDTHH:MM:SSZ] [req_id=<ID>] HTTP <STATUS>`
   - Timezone: UTC (ISO 8601 format)
   - Example: `[2023-10-25T14:32:01Z] [req_id=REQ-001] HTTP 200`

2. **Auth Service** (`/home/user/logs/auth_service.log`)
   - Format: `<EPOCH_TIMESTAMP> - tx_id:<ID> - <MESSAGE>`
   - Timezone: UTC (Epoch Unix timestamp as a float)
   - Example: `1698244321.150 - tx_id:REQ-001 - Authenticated successfully`

3. **Payment Backend** (`/home/user/logs/payment_backend.log`)
   - Format: `YYYY/MM/DD HH:MM:SS | trace=<ID> | STATE: retry_count=<N> | <MESSAGE>`
   - Timezone: EDT (Eastern Daylight Time, UTC-4). Note: the logs just show the local time, there is no timezone identifier in the line itself.
   - Example: `2023/10/25 10:32:01 | trace=REQ-001 | STATE: retry_count=0 | Payment processed`

### The Intermittent Failure

Through preliminary investigation, we know the failure occurs when:
1. The Payment Backend reaches a `retry_count` of `3` or higher for a single transaction.
2. This is subsequently followed by the API Gateway logging an `HTTP 503` for that exact same request ID.

### Your Task

1. Write a Python script at `/home/user/reconstruct.py` that reads the three log files.
2. The script must parse and correlate the logs across all three services using the request/transaction ID (`req_id`, `tx_id`, `trace`).
3. Identify all request IDs that match the intermittent failure conditions described above.
4. Your script must generate an output file at `/home/user/failed_traces.json`. This file must contain a single JSON array of strings, representing the request IDs that failed, sorted in ascending alphabetical order.
   - Example output format: `["REQ-042", "REQ-105", "REQ-899"]`

You may install any standard Python packages (like `pytz`) if needed, though standard library modules should be sufficient. Run your script to generate the required JSON file.
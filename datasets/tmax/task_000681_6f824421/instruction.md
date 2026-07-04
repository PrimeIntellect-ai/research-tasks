I am a data scientist working on cleaning a batch of legacy system logs, but the data is incredibly messy and contains PII. I need you to process this raw dataset and spin up a lightweight data-access service for our internal validation tools.

You are provided with a raw log file at `/home/user/raw_syslogs.txt`. 
Each line in this file has the following loosely structured format:
`[TIMESTAMP] source_ip=<IP> user=<EMAIL> payload=<JSON_STRING>`

Here are your objectives:
1. **Timestamp Alignment**: The `TIMESTAMP` field is messy (mixing `Mon DD HH:MM:SS YYYY`, `YYYY/MM/DD HH:MM:SS`, etc.). You must parse and align all timestamps to standard ISO-8601 UTC format (`YYYY-MM-DDTHH:MM:SSZ`).
2. **Structured Information Extraction**: Extract the JSON string from the `payload` field.
3. **Data Masking**: You must anonymize the `<EMAIL>` field. There is a proprietary, stripped legacy binary located at `/app/anonymizer`. It acts as a black-box hashing oracle. Figure out how to invoke it to generate a consistent hash for each email address.
4. **Data Serving**: You must write a Bash script `/home/user/serve_cleaned.sh` that uses standard shell tools (like `nc` or `socat`) to listen for TCP connections on `127.0.0.1:8333`. 
   - The service must accept a TCP string request in the format: `FETCH <ANONYMIZED_EMAIL>\n`
   - It must respond with all cleaned log lines associated with that anonymized email, one per line, sorted chronologically by the new ISO-8601 timestamp.
   - The output format for each returned line must be strictly: `TIMESTAMP | ANONYMIZED_EMAIL | JSON_STRING`
   - The service should remain running and handle multiple sequential requests.

Please create the processing script, generate the cleaned dataset internally, and start the TCP service. Leave the service running in the background on port 8333.
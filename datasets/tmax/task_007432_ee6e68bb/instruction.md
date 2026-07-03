You are a configuration manager responsible for tracking deployment changes across a fleet of servers. The system logs every configuration update applied to the servers in a text file.

You have a log file located at `/home/user/config_changes.log`. Each line in this file represents a configuration update and follows this exact format:
`[YYYY-MM-DD HH:MM:SS] IP=<ipv4_address> PAYLOAD={<configuration_string>}`

Your task is to write a Go program at `/home/user/analyzer.go` that performs the following steps:
1. Reads the `/home/user/config_changes.log` file.
2. Uses regular expressions to extract the exact `<configuration_string>` inside the `PAYLOAD={...}` block for each line.
3. Computes the SHA-256 hash (in lowercase hexadecimal format) of the extracted `<configuration_string>`.
4. Uses hash-based deduplication to count how many times each unique configuration payload was applied across the fleet.
5. Outputs the results to a JSON file at `/home/user/unique_configs.json`. The JSON file must be a single flat object where the keys are the SHA-256 hashes and the values are the integer counts of how many times that specific payload appeared. 

Example output format for `/home/user/unique_configs.json`:
```json
{
  "f1870df22bd5734267e71f9cf741e9dc866a4bc2a452bf5ccfbf7f433ea3504d": 3,
  "524fcc160161494eb75e8efca42b104dc2542a2082269a8433436d4df61f23ee": 1
}
```

Write the Go program, run it, and ensure the JSON file is created successfully with the correct data.
You are an SRE tasked with automating the retrieval and processing of uptime logs from a secure, interactive legacy service.

You have been provided with a mock fstab file at `/home/user/mock_fstab`.

Your tasks are:

1. **Automate Interactive Retrieval (Expect):**
There is a secure logging service located at `/home/user/vault_log_fetch`. It is an interactive program that prompts for credentials before outputting the raw downtime logs.
Write an `expect` script at `/home/user/auto_fetch.exp` that executes `/home/user/vault_log_fetch`, waits for the prompt `Username: `, sends `sre_admin`, waits for the prompt `PIN: `, and sends `998877`. 
Capture the output (which consists of UTC downtime events) and save it to a file named `raw_logs.txt` inside the directory specified for `/dev/sda1` in the `/home/user/mock_fstab` file. You must parse or inspect the fstab file to determine this directory. Make sure to create the directory if it does not exist.

2. **Process and Timezone Conversion (Go):**
Write a Go program at `/home/user/analyzer.go` that does the following:
- Reads `/home/user/mock_fstab` to dynamically determine the mount point for `/dev/sda1`.
- Reads the `raw_logs.txt` file from that directory.
- For each log line, parse the ISO8601 UTC timestamp and the event message. (Format: `YYYY-MM-DDTHH:MM:SSZ | Event message`)
- Convert the timestamp to the `Asia/Tokyo` timezone.
- Write the results to a file named `processed_logs.txt` in the same mount point directory. 
- The output format for each line must strictly be: `YYYY-MM-DD HH:MM:SS JST - Event message`

**Example of raw log line:**
`2023-11-05T08:30:00Z | Network partition`
**Expected processed line:**
`2023-11-05 17:30:00 JST - Network partition`

Ensure your Go program is completely self-contained, compiles, and runs successfully using `go run /home/user/analyzer.go`. When you are done, execute your expect script followed by your Go program so the final `processed_logs.txt` file is generated.
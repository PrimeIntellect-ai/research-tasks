As an observability engineer, you need to set up a metrics processing pipeline to feed our new dashboard. 

We have two existing services that are part of this pipeline, but they are currently disconnected and missing the middle processing component.
1. `app_mock.service`: A user systemd service running a mock application that emits raw metrics over UDP to port 8125.
2. `dashboard.service`: A user systemd service running a dashboard API that listens on HTTP port 9090 for processed metrics.

Your tasks are as follows:

1. **Service Management**: 
   The `app_mock` and `dashboard` services have been placed in `/home/user/.config/systemd/user/` but are not running. Enable and start them. Ensure they automatically restart if they fail.

2. **Write the Metric Parser in C**:
   The `app_mock` emits metrics in a legacy custom format. You must write a C program that parses a single line of this format from standard input (stdin) and prints a strict canonical representation to standard output (stdout).
   Save your source code as `/home/user/parser.c` and compile it to `/home/user/parser`.

   *Input Format:* `<metric_name>:<value>|<type>|#<tag_key>:<tag_value>,<tag_key>:<tag_value>...`
   *Example Input:* `cpu_load:2.45|gauge|#host:server1,env:prod`
   
   *Output Format:* `NAME=[<metric_name>] TYPE=[<type>] VALUE=[<value_formatted_to_4_decimal_places>] TAGS=[<key>=<value>;<key>=<value>;...]`
   *Example Output:* `NAME=[cpu_load] TYPE=[gauge] VALUE=[2.4500] TAGS=[host=server1;env=prod;]`

   *Constraints:*
   - Input line will be at most 256 characters, terminated by a newline.
   - Value is a float.
   - Print a newline at the end of the output.
   - If the input does not perfectly match the format (e.g., missing fields, missing tags), output exactly `INVALID_METRIC\n`.
   - Preserve the original order of the tags.

3. **Build the Aggregator script**:
   Write a bash script at `/home/user/aggregator.sh` (make it executable). This script should:
   - Listen for UDP packets on port 8125.
   - Pass the received packet through your `/home/user/parser` executable.
   - If the output is not `INVALID_METRIC`, send the parsed output string as the HTTP POST body to `http://localhost:9090/ingest` with a `Content-Type: text/plain` header.
   - The script should run continuously in a loop, handling one packet at a time, robust against errors.

4. **Run the Aggregator**:
   Create a user systemd service for your aggregator script at `/home/user/.config/systemd/user/aggregator.service` and start it so the end-to-end pipeline is active.

Please complete all these steps. The verification will fuzz test your C program against a reference implementation to ensure exact bit-equivalence, and will also send test metrics through the end-to-end pipeline to verify the dashboard receives the correctly formatted data.
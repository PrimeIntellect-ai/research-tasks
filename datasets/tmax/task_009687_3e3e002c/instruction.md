You are a log analyst investigating intermittent performance degradation on a web server. You need to write a C++ tool to parse a log file, compute rolling statistics to detect latency spikes, and generate templated alert messages.

A log file is located at `/home/user/server.log`. Each line follows this exact format:
`[YYYY-MM-DDThh:mm:ssZ] <METHOD> <ENDPOINT> <LATENCY_MS>`
Example:
`[2023-10-15T14:32:01Z] GET /api/v1/users 150`

Your objective is to write and execute a C++ program at `/home/user/analyze.cpp` that does the following:
1. **Regex Parsing:** Read `/home/user/server.log` line by line. Use the `<regex>` library to extract the `<ENDPOINT>` and the integer `<LATENCY_MS>`.
2. **Rolling Statistics:** For *each* unique endpoint, maintain a rolling window of the last 3 latency values. Compute the integer rolling average (using integer division) every time a new latency value is added to that endpoint's window. Do not compute an average until a full window of 3 values has been collected for that endpoint.
3. **Template-based Generation:** Whenever an endpoint's rolling average latency reaches or exceeds `500` ms, generate an alert. You must write a simple template replacement function that takes the template string:
   `"ALERT: {{ENDPOINT}} is experiencing degradation. Current 3-request rolling average is {{AVG}}ms."`
   and replaces `{{ENDPOINT}}` and `{{AVG}}` with the respective values.
4. **Output:** Write all generated alert messages, in the exact order they occurred, to `/home/user/alerts.txt`, one per line.

Requirements:
- Compile your program to `/home/user/analyze` using `g++ -std=c++17 /home/user/analyze.cpp -o /home/user/analyze`.
- Run the program to process the logs and generate `/home/user/alerts.txt`.
You have been tasked with building a configuration state server for our distributed mathematical compute nodes. The system tracks configuration changes over time, but the existing logs are messy and require careful data processing.

You are provided with two artifacts:
1. `/app/authorization_pin.wav`: An audio recording containing the spoken 4-digit PIN required to authorize API requests. You must transcribe this.
2. `/app/config_events.jsonl`: A JSON-lines log file containing historical configuration updates. 

**Data Processing & Rules:**
* Parse `/app/config_events.jsonl`. Be warned: the system that wrote this file had a bug where it occasionally wrote invalid standalone unicode surrogates (e.g., `\ud800`) in the `comment` field, which breaks standard strict JSON parsers. You must gracefully handle or sanitize these character encoding issues without dropping the data.
* Each valid line contains: `node_id` (string), `timestamp` (integer), `operation` (string: "add" or "multiply"), `vector` (list of 3 integers), and `comment` (string).
* Group the events by `node_id` and sort them strictly by `timestamp` in ascending order.
* Calculate the final state vector for each node. All nodes start with a state vector of `[0, 0, 0]`.
    * `add`: Add the event's vector to the current state vector element-wise.
    * `multiply`: Multiply the current state vector by the event's vector element-wise.
* **Constraint Validation:** After calculating the final state for a node, you must validate it. If the sum of the squares of the final vector's components exceeds `1,000,000`, the configuration is considered unstable, and the node's state must be completely discarded (it should not be available in the API).

**Service Requirements:**
Write a Python script that processes the data and then starts an HTTP server (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`.
The server must implement a single endpoint:
* `GET /state/<node_id>`
* It must require an HTTP header named `X-Auth-Pin` containing the exact 4-digit numeric string spoken in `/app/authorization_pin.wav`. If the header is missing or incorrect, return a `401 Unauthorized` HTTP status.
* If the node exists and is valid, return a `200 OK` status with a JSON body: `{"node_id": "<node_id>", "state": [x, y, z]}`.
* If the node does not exist or was discarded due to the constraint validation, return a `404 Not Found`.

Leave the server running in the foreground so it can be tested.
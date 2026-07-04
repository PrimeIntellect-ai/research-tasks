You are a data engineer responsible for building an ETL pipeline to process raw drone flight logs. 

We receive unstructured text logs containing telemetry data, and we need to extract this data, process it, and find the drone that flew closest to our central delivery depot.

The central delivery depot is located at coordinates:
Latitude: `45.5000`
Longitude: `-122.6000`

The raw logs are located at `/home/user/flight_data.log`. 
A typical log line looks like this:
`[2023-11-01 10:15:22] INFO Drone ID: D-404 | Status: OK | Pos: 45.5100, -122.6100 | Payload: 2.5kg`
Some lines may be error lines without position data, for example:
`[2023-11-01 10:16:00] ERROR Drone ID: D-405 | Status: OFFLINE | Connection Lost`

Your task is to write a single Bash orchestration script at `/home/user/process_flights.sh` that does the following:
1. Extracts the Drone ID, Latitude, and Longitude from all valid `INFO` lines containing `Pos: <lat>, <lon>`.
2. Calculates the Euclidean distance from each drone's position to the central delivery depot.
3. Identifies the drone that is closest to the depot.
4. Outputs the result as a JSON file at `/home/user/closest_drone.json`.

The JSON file must have exactly this format:
```json
{
  "closest_drone": "D-XXX",
  "distance": 0.00
}
```
(Note: Round the distance to 4 decimal places).

Requirements:
- Install any necessary dependencies (like `jq`, `bc`, or `awk` if needed) using `sudo apt-get` (assuming standard Ubuntu environment where the agent user has passwordless sudo). *Wait, you don't have root access in this environment, but standard tools like `awk`, `grep`, `sed`, `bc`, and `jq` are usually pre-installed. Do not try to run `sudo`.*
- Ensure `/home/user/process_flights.sh` is executable and run it to generate the final JSON.
- Use standard bash tools (awk, sed, grep, etc.) for the extraction and computation pipeline.
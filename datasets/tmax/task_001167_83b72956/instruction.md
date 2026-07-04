You are a support engineer tasked with collecting diagnostics for a failing telemetry pipeline on a Linux system.

In `/home/user/telemetry_diag`, there are two main components:
1. `sensor_dummy`: A pre-compiled proprietary binary that generates sensor readings. 
2. `agent.cpp`: A C++ program that invokes the sensor, reads the raw data, and calculates the Root Mean Square (RMS) of the readings.

Currently, the pipeline is failing in two ways:
1. **Garbled Queries:** The `agent.cpp` program complains that the sensor is returning binary garbage instead of parsable integer readings. You must figure out how to configure the environment so that `sensor_dummy` outputs plaintext diagnostic integers. You don't have the source code for `sensor_dummy`, so you will need to inspect the binary to find the hidden configuration flag (e.g., an environment variable) it expects.
2. **Intermittent Formula Bug:** Once the agent can parse the plaintext data, it crashes or returns incorrect results during high-load scenarios. The `agent.cpp` code calculates the RMS of the values. There is a bug in the implementation of the formula that manifests only when the sensor outputs very large values (which happens intermittently, specifically with the sequence of values the diagnostic mode outputs). 

**Your tasks:**
1. Determine the missing environment variable required by `sensor_dummy` to output plaintext data, and modify `agent.cpp` or your run environment so the agent sets it before reading the data.
2. Identify and fix the mathematical implementation bug in `agent.cpp` causing the intermittent failure with high values.
3. Recompile the agent as `agent_fixed` in the `/home/user/telemetry_diag` directory.
4. Run the compiled agent and redirect its standard output to `/home/user/telemetry_diag/diagnostic_report.txt`.

The final `diagnostic_report.txt` should contain exactly the text output by the fixed C++ program.
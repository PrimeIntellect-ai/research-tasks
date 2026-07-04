You are an automation specialist modernizing a sensor data pipeline. Our system receives wide-format telemetry data, but our legacy anomaly detection engine only accepts long-format data.

Your objective is to build a C++ TCP server that validates incoming data, reshapes it, queries a proprietary legacy binary for a similarity/distance score, and returns the result. You also need to define a cron schedule for batch jobs.

**Task Requirements:**

1. **TCP Service (`/home/user/sensor_server.cpp`):**
   - Write and compile a C++ TCP server that listens on `127.0.0.1:7777`.
   - The server must accept incoming client connections and read single-line wide-format CSV strings formatted as: `RECORD_ID,X_VAL,Y_VAL,Z_VAL\n` (e.g., `A102,12.5,-3.0,42.1\n`).
   - The compiled executable must be saved at `/home/user/sensor_server` and you must leave it running in the background.

2. **Constraint Validation:**
   - For each request, parse the CSV. Validate that `X_VAL`, `Y_VAL`, and `Z_VAL` are all floating-point numbers between `-100.0` and `100.0` (inclusive).
   - If any value is out of bounds, or if the format is incorrect, respond to the TCP client with exactly: `ERR: INVALID_DATA\n` and close the connection.

3. **Wide-Long Reshaping & Legacy Binary:**
   - If the data is valid, reshape it into a long-format string. The legacy binary at `/app/dist_calc` (which is already provided in the environment as a stripped executable) computes a proprietary distance metric.
   - It expects standard input in the following three-line long format:
     ```
     <RECORD_ID> X <X_VAL>
     <RECORD_ID> Y <Y_VAL>
     <RECORD_ID> Z <Z_VAL>
     ```
     *(Example: `A102 X 12.5\nA102 Y -3.0\nA102 Z 42.1\n`)*
   - Your C++ server must spawn the `/app/dist_calc` process, feed the long-format string to its `stdin`, and read its `stdout` (which will be a single float value followed by a newline).

4. **Response:**
   - The C++ server must return the computed score to the TCP client formatted as: `SCORE: <value>\n` (e.g., `SCORE: 45.21\n`) and then close the connection.

5. **Cron Management:**
   - Create a crontab file at `/home/user/pipeline_cron`.
   - Add exactly one valid cron expression that schedules the script `/home/user/batch_poll.sh` to run every 5 minutes, every day. (You do not need to create the script itself, just the cron schedule file).

Ensure your C++ server manages zombie processes properly or waits on the child process to prevent resource leaks. Use standard POSIX headers (`<sys/socket.h>`, `<unistd.h>`, etc.) and standard C++ libraries.
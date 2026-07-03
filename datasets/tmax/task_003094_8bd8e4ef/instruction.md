As a compliance officer, I am auditing our isolated environment's legacy visual-log system. Bizarrely, access logs were encoded into an MP4 video file located at `/app/audit_log.mp4` (128x128 resolution).

Each frame in the video represents a single access event in chronological order. The color of the exact center pixel (x=64, y=64) encodes the details:
- **Red channel (R)**: Source Employee ID (0-255)
- **Green channel (G)**: Target System ID (0-255)
- **Blue channel (B)**: Access Status (1 = Granted, 0 = Denied)

I need you to create a Rust project at `/home/user/audit_query` that acts as a graph projection and querying tool. The compiled binary should accept two command-line arguments: `start_frame` and `end_frame` (inclusive).

Your program must:
1. Extract the center pixel RGB values for the specified frame range from `/app/audit_log.mp4`. (You may invoke `ffmpeg` via sub-processes or use any suitable Rust crate).
2. Materialize a directed graph in memory of only the **Granted** accesses (B=1). An edge goes from the Employee ID (R) to the Target System ID (G).
3. Query this graph to find the Employee ID with the highest out-degree (the employee who successfully accessed the most systems in that time window). If there is a tie, select the lowest Employee ID.
4. Print exactly `<Employee_ID>,<Out_Degree>` to stdout and exit.

Requirements:
- Your Rust code must be compiled in release mode. The final executable must be located at `/home/user/audit_query/target/release/audit_query`.
- The system will automatically test your binary using a fuzzing verifier. It will generate random `start_frame` and `end_frame` pairs and compare your output bit-for-bit against a highly optimized reference implementation.

Please write the Rust code, manage any necessary dependencies, and ensure the project builds successfully.
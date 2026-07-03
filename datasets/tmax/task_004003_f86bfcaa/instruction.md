You are a data scientist tasked with cleaning a drone telemetry dataset before it is released to the public. The dataset consists of flight videos and streamed JSON logs. You must perform two tasks: identify corrupted video frames and write a robust log sanitiser in Rust.

**Part 1: Video Corruption Detection**
The flight video is located at `/app/flight_video.mp4`. Due to a sensor glitch, some frames in the video are completely pure red (every pixel is exactly `RGB(255, 0, 0)`). 
1. Analyze the video and identify the 0-indexed frame numbers of these completely red frames.
2. Write these frame numbers to `/home/user/red_frames.txt`, with one frame number per line in ascending order.
*(Hint: You can use `ffmpeg` to extract frames or analyze them programmatically.)*

**Part 2: Log Sanitisation Pipeline**
You need to build a Rust application that processes large streaming log files and filters out sensitive or anomalous data.
1. Initialize a Rust project at `/home/user/log_filter`.
2. Write a Rust CLI program that reads JSON Lines from standard input (`stdin`) and writes the allowed JSON Lines to standard output (`stdout`).
3. Your program must efficiently stream the data and **drop (do not print)** any JSON line that meets **any** of the following criteria:
   - It contains a top-level key `"military_zone"` with the boolean value `true`.
   - The top-level `"device_id"` string matches a standard MAC address format (exactly 6 groups of 2 uppercase or lowercase hex digits separated by colons, e.g., `0A:1B:2C:3d:4e:5F`).
   - The top-level `"battery_temp"` is a number strictly greater than `90.0`.
4. All other valid JSON lines must be printed to `stdout` exactly as they were read (or functionally equivalent JSON). Lines that cannot be parsed as JSON should be dropped.
5. Compile your program in release mode so the final executable is at `/home/user/log_filter/target/release/log_filter`.

We will test your binary against a hidden "clean" corpus and a hidden "evil" corpus. To pass, your program must preserve 100% of the clean corpus and reject 100% of the evil corpus. You can test your assumptions using standard Rust libraries (`serde_json`, `regex`, etc.).
You are a Site Reliability Engineer investigating a recent series of severe outages and telemetry corruption in our legacy mathematical heartbeat monitor. You have two distinct assignments to resolve the monitoring pipeline issues.

**Part 1: Visual Heartbeat Analysis**
Our legacy system outputs its uptime heartbeat as a video feed. We have captured the latest outage in `/app/uptime_feed.mp4`. The video displays a solid green frame when the system is healthy, and a solid red frame when the system is down. 
Use `ffmpeg` (which is preinstalled) and any necessary shell commands to analyze the video. Identify all exact frame indices where the video is solid red (down). Write the frame numbers, one per line in ascending order, to `/home/user/downtime_frames.txt`.

**Part 2: Telemetry Data Sanitization**
Our log aggregation pipeline is crashing due to malformed and maliciously crafted telemetry logs. You must write a bash script to classify whether a telemetry file is "clean" or "evil".
Create a Bash script at `/home/user/detector.sh`. It must take a single file path as its argument.
It must exit with code `0` if the file is completely clean, and exit with code `1` if the file is evil.

A log line format is: `[ID] <UptimeSecs> | Load_A:Load_B | Checksum`
Example: `[104] 3450 | 12.5:8.1 | 55`

To be considered "clean", EVERY line in the file must strictly satisfy all of the following mathematical and boundary conditions:
1. `ID` must be a strictly positive integer, and in a multi-line file, `ID`s must strictly increase by exactly 1 for each subsequent line.
2. `UptimeSecs` must be a non-negative integer.
3. `Load_A` and `Load_B` are floating point numbers.
4. The `Checksum` must exactly equal the modulo 100 of the sum of `ID`, `UptimeSecs`, the floor of `Load_A`, and the ceiling of `Load_B`. 
   Formula: `Checksum = (ID + UptimeSecs + floor(Load_A) + ceil(Load_B)) % 100`

"Evil" files contain edge cases such as:
- Off-by-one errors in the ID sequence.
- Incorrect mathematical checksums due to improper floor/ceiling boundaries (e.g., negative numbers rounding incorrectly).
- Format parsing edge cases (e.g., extra whitespaces, missing brackets).

Your script must perfectly differentiate between clean and evil logs. We will test it against a hidden corpus.
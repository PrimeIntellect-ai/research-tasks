**Ticket ID:** IT-9923
**Subject:** `data_processor` crashing on weekly sensor payload
**From:** Data Science Team

Hi Support,

We have a legacy compiled binary located at `/home/user/data_processor`. It processes our binary sensor logs. Unfortunately, the original source code was lost years ago. 

When we try to run it on this week's data file (`/home/user/sensor_data.bin`), the program crashes with a segmentation fault. We suspect the sensor occasionally outputs a specific corrupted 4-byte sequence that triggers a fatal bug (likely an unhandled edge case or overflow) in the processor, causing convergence failure in the downstream pipeline.

Your task:
1. Reverse engineer or analyze the `/home/user/data_processor` binary to determine the exact 4-byte corrupted sequence that causes it to crash. 
2. Write a Rust program at `/home/user/recover.rs` that reads `/home/user/sensor_data.bin`, replaces all instances of this specific 4-byte corrupted sequence with zeroes (`0x00 0x00 0x00 0x00`), and writes the cleaned data to `/home/user/cleaned_data.bin`.
3. Compile and run your Rust program.
4. Run the legacy processor on the cleaned file and redirect its standard output to `/home/user/report.txt`:
   `./data_processor /home/user/cleaned_data.bin > /home/user/report.txt`

Please ensure `/home/user/report.txt` is successfully generated and the program exits cleanly.
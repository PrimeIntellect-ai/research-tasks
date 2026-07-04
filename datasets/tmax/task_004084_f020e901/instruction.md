We are experiencing a critical issue in our telemetry processing pipeline. As a performance engineer, I need you to investigate a regression that causes our data extraction tool to produce corrupted output and leak memory. 

You have access to a local Git repository at `/home/user/telemetry-processor`. There is a known good commit (`v1.0`) and a known bad commit (`HEAD`). 

1. **Regression Finding**: Use `git bisect` to identify the exact commit that introduced the memory leak and statistical anomalies in the telemetry output. Write the hash of the bad commit to `/home/user/bad_commit.txt`.
2. **Memory Dump Analysis**: Inside `/app/coredump.dat` is a memory dump from a crashed instance. Extract the corrupted input handling configuration string (format: `CFG-[A-Z0-9]{8}`) and save it to `/home/user/config_string.txt`.
3. **Audio Fixture Processing**: We captured an audio signal from the system before it crashed at `/app/telemetry.wav`. Use standard Bash tools to extract the hidden sequence of 4-digit numeric codes spoken in the audio file. Write these codes, one per line, to `/home/user/audio_codes.txt`.
4. **Fuzz Equivalence Script**: After diagnosing the numerical instability and input parsing bugs introduced in the bad commit, write a new Bash script at `/home/user/parse_telemetry.sh` that exactly matches the behavior of the `v1.0` binary. Your script must read a corrupted telemetry string from standard input, handle the anomalies according to the logic found in the good commit, and print the corrected output to standard output. 

Your `parse_telemetry.sh` script will be strictly verified against the `v1.0` binary using a fuzz-equivalence tester with thousands of random corrupted inputs. Ensure it is perfectly bit-exact in its output.
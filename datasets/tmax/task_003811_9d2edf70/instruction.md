Wake up! It's 3:00 AM and you are the primary on-call engineer. We just got a PagerDuty alert that the critical telemetry ingestion pipeline has crashed and the data backlog is building up.

Here is what we know:
1. The ingestion service is started via `/home/user/bin/start.sh` and logs its output to `/home/user/logs/ingester.log`. It seems to be crashing immediately upon startup.
2. The core binary `/home/user/bin/data_ingester` is a compiled legacy executable. We don't have the source code readily available.
3. Because the service is down, a backlog of encrypted telemetry data has accumulated at `/home/user/data/backlog.enc`.

Your objectives to resolve this incident are:
1. **Fix the Environment:** Investigate why `/home/user/bin/data_ingester` is crashing by checking its logs and startup script. Fix the misconfiguration in `/home/user/bin/start.sh` so that running it no longer results in a crash.
2. **Reverse Engineer the Key:** The binary contains a hardcoded XOR key used for data decryption. Extract this key from the compiled binary. It is stored as a string in the format `XOR_KEY=<key_value>`.
3. **Process the Backlog:** Write a script (in Python, Ruby, Perl, or any language you prefer) to manually decrypt the file `/home/user/data/backlog.enc`. The file is encrypted by performing a repeating byte-wise XOR against the `<key_value>` string (just the value, not the "XOR_KEY=" part).
4. **Document the Resolution:** Save the decrypted ASCII message to `/home/user/data/processed.txt`. Additionally, create a final report at `/home/user/resolution.txt` containing exactly two lines:
   - Line 1: The extracted `<key_value>`
   - Line 2: The fully decrypted telemetry message

Time is of the essence. Get the service working and decrypt that data!
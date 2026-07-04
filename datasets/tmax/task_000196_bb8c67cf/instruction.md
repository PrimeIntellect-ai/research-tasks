You are a data scientist tasked with migrating our legacy dataset cleaning ETL pipeline to a new, native Go implementation. 

We process high-frequency sensor data, but our initial preprocessing step (which filters outliers and scales the features) is currently handled by a highly optimized but completely undocumented legacy C binary. We no longer have the source code for this binary, but we have a stripped version of it located at `/app/legacy_cleaner`.

Your objective is to:
1. Reverse-engineer or black-box analyze the `/app/legacy_cleaner` binary to understand the mathematical transformation it applies to the data. It reads space-separated floating-point numbers from standard input and outputs the transformed floating-point numbers to standard output, space-separated, with 6 decimal places of precision.
2. Write a Go program at `/home/user/cleaner.go` that implements exactly the same mathematical transformation. It must read and write in the exact same format as the legacy binary.
3. Build your Go program into an executable located at `/home/user/go_cleaner`.
4. As part of the ETL pipeline construction, create an initialization script at `/home/user/setup_db.sh` that sets up a local PostgreSQL database named `sensor_data`, with a table `cleaned_features` containing columns `id (SERIAL)` and `value (FLOAT8)`.

The automated verifier will randomly generate sequences of floats and pass them to both `/app/legacy_cleaner` and your `/home/user/go_cleaner`. To succeed, your Go program's output must be bit-exact equivalent to the legacy binary's output for any valid float input.
You are an automation specialist creating a data processing workflow. We use a Rust-based tool to parse JSON-lines telemetry data, compute rolling statistics, and deduplicate records before passing them to our orchestration DAG. 

We have a pre-vendored Rust package located at `/app/vendored/telemetry-processor`. However, the package currently cannot build or run due to a deliberate perturbation in its build setup (the `Makefile` is broken and passes incorrect flags, and `Cargo.toml` has a configuration error). 

Your task:
1. Identify and fix the build errors in `/app/vendored/telemetry-processor` so that `make build` successfully compiles the release binary.
2. Implement the missing sanitization and filtering logic in `src/main.rs`. The program must read a JSON-lines file (provided via the first command-line argument) and output the valid, processed records to standard output (one JSON object per line).

The filtering and processing requirements are:
- **Sanitization**: Reject (do not output) any JSON line that contains unescaped control characters or invalid unicode escape sequences (such as lone surrogates like `\uDEAD`). 
- **Normalization & Cleaning**: Reject any record where the `value` field is not a number between `0.0` and `1000.0` inclusive.
- **Deduplication**: Reject any record if it has the exact same `sensor_id` and `message` as the *most recently accepted* record for that specific `sensor_id`.
- **Rolling Statistics**: For accepted records, calculate a rolling moving average of the `value` field over the last 3 accepted records for that `sensor_id`. Append this to the output JSON as `"rolling_avg"`. If fewer than 3 records exist for a sensor, compute the average of the available ones.

The output should just be valid JSON-lines printed to stdout.

To succeed, your compiled binary (`/app/vendored/telemetry-processor/target/release/telemetry-processor`) must perfectly distinguish between clean and malicious/malformed inputs. The automated verification suite will test your binary against two hidden directories of corpora:
- A `clean` corpus, where 100% of the records must be processed and output.
- An `evil` corpus, where 100% of the records must be rejected (no output generated).
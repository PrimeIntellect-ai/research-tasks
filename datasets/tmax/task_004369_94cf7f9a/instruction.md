As a platform engineer maintaining our CI/CD pipelines, I am dealing with a pipeline failure caused by a schema mismatch. Our edge devices are sending telemetry data using an older Protocol Buffers schema (`v1`), but our backend testing environment now strictly requires the `v2` schema. The local test suite passes because it mocks the data in Python, but the CI pipeline fails when attempting to process the actual binary artifacts sent by the devices.

Your task is to implement a C program that performs a schema migration on the serialized protobuf data.

You have been provided with:
1. `/home/user/schemas/v1.proto` - The old schema.
2. `/home/user/schemas/v2.proto` - The new schema.
3. `/home/user/data/input_v1.bin` - A binary file containing a single serialized `TelemetryV1` message.

You must:
1. Create a C program at `/home/user/migrate.c`.
2. Use the `protobuf-c` library to deserialize the message from `/home/user/data/input_v1.bin`.
3. Migrate the data to the `TelemetryV2` format based on these rules:
   - `device_id` and `temperature` remain exactly the same.
   - The string `status_code` in `v1` must be mapped to the `Status` enum in `v2`: map `"OK"` to `OK`, `"ERR"` to `ERROR`. Any other string maps to `UNKNOWN`.
   - The new `timestamp` field in `v2` must be set to the hardcoded integer `1710000000`.
4. Serialize the migrated `TelemetryV2` message and write the raw binary output to `/home/user/data/output_v2.bin`.
5. Write a summary log file to `/home/user/migration.log` containing exactly one line with the format: `Migrated device <device_id> to status enum <status_integer>`.

You will need to install any necessary protobuf C compilers and libraries (e.g., `protobuf-c-compiler`, `libprotobuf-c-dev`). Compile your C program and execute it so that the output files are generated.
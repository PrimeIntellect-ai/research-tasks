You are an operations engineer triaging a recent incident. A background Go service responsible for parsing telemetry data has been crashing repeatedly with a slice bounds out of range panic. 

We have captured a partial memory dump of the process right before the crash, located at `/home/user/dump.bin`. 

Your tasks are:
1. Analyze the `/home/user/dump.bin` file to extract the exact corrupted telemetry string that caused the panic. Telemetry strings always start with `ID:`. Save this exact string into `/home/user/corrupted_string.txt` (without any trailing newline if possible, just the string itself).
2. Fix the telemetry parsing logic in `/home/user/processor/processor.go`. The function `ProcessTelemetry(data string) map[string]string` splits the data by `|` to get key-value pairs, and then by `:` to separate the key from the value. It currently assumes every field has a `:`, causing a panic if a corrupted field does not. Update the function to safely ignore any fields that do not contain a `:` character (do not add them to the map), preventing the panic.
3. Write a regression test in `/home/user/processor/processor_test.go`. The test must call `ProcessTelemetry` passing the exact corrupted string you found in the dump, and verify that the function completes without panicking and returns the successfully parsed fields.

Ensure your code is properly formatted and passes tests. You can test your changes by running `go test` in the `/home/user/processor` directory.
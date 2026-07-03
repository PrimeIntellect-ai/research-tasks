You have inherited an unfamiliar Go codebase located in `/home/user/telemetry` that processes drone flight data. The previous developer left suddenly, and the data ingestion pipeline is currently failing in production. 

There are two major issues you need to resolve:
1. **Intermittent Panics:** The function `ParseLine(line string)` in `parser.go` occasionally panics and crashes the entire microservice. The input format is supposed to be `Timestamp,Latitude,Longitude,Altitude`, but edge-case or malformed data strings cause it to crash.
2. **Floating-Point Precision Loss:** The `Point` struct and distance calculations currently use `float32`. This has caused accumulated tracking drift. 

Your tasks are to:
1. **Fuzz Test:** Write a standard Go fuzz test named `FuzzParseLine` in `/home/user/telemetry/parser_test.go` that targets `ParseLine(line string)`. Run the fuzzer to reproduce the panic.
2. **Fix the Parsing Panic:** Modify `ParseLine` in `parser.go` so that it safely handles malformed lines (e.g., fewer than 4 comma-separated parts, or invalid float values). It should return an error instead of panicking or ignoring parse errors.
3. **Repair Floating-Point Precision:** Upgrade the `Lat`, `Lon`, and `Alt` fields in the `Point` struct to `float64`. Update `ParseLine` and `Distance(p1, p2 *Point) float64` to use `float64` exclusively to prevent precision loss.
4. **Verification:** Create a script at `/home/user/verify.go` that imports your package, parses the following two lines, calculates the distance between them using your updated `Distance` function, and writes the output formatted exactly with `%v` to `/home/user/distance_result.txt`.

Lines to parse in `verify.go`:
Line 1: `"2023-01-01T00:00:00Z,45.123456789,-90.123456789,100.0"`
Line 2: `"2023-01-01T00:00:01Z,45.123456700,-90.123456700,100.0"`

Ensure your fixes allow `go test` and `go test -fuzz=Fuzz` to run without panicking.
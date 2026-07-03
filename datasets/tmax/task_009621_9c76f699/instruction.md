PagerDuty Alert: `CRITICAL - log-ingester crash loop on production batch 491`

It's 3:00 AM and our Go-based custom log ingestion service is continuously panicking when processing a newly arrived batch file. The service is supposed to parse a custom key-value log format, validate the intermediate objects, and output a JSON array of the parsed records.

You need to investigate the crash in the `log-ingester` service located at `/home/user/ingester`.

Here is your incident response plan:
1. **Delta Debugging / Minimization:** The problematic batch file is located at `/home/user/data/batch_491.log`. It contains 10,000 log lines, but only *one* specific line is triggering the panic. Use bisection/delta debugging techniques to isolate the exact single line that causes the Go program to panic. Save this single line to `/home/user/minimal_crash.log`.
2. **Format Parsing Edge-Case Repair:** Analyze the panic stack trace and the minimal crash line. The custom parser in `/home/user/ingester/parser/parser.go` has a bug when handling specific edge cases involving escaped quotes inside quoted strings. Fix the parser so it handles this edge case without panicking and correctly extracts the value.
3. **Assertion-Based Validation:** The pipeline currently lacks intermediate validation before JSON serialization. Modify `/home/user/ingester/processor/processor.go`. In the `Process` function, add an assertion: if the parsed `UserAgent` field is empty for any record, it must return an error `fmt.Errorf("validation failed: empty user agent")` rather than proceeding.
4. **Build and Execute:** Ensure `go test ./...` passes in the `/home/user/ingester` directory. Once fixed, run the ingester on the full file: `go run main.go -input /home/user/data/batch_491.log -output /home/user/output.json`.

Ensure your final `output.json` contains the successfully parsed JSON array of all 10,000 lines, and `minimal_crash.log` contains exactly the one unparsed string.
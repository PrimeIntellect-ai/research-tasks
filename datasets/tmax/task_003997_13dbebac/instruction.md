You are a support engineer investigating a bug for a client. The client has provided a vendored Go package located at `/app/telemparser` which reads their proprietary encrypted telemetry data and calculates the statistical mean of the recorded values. 

Recently, clients have reported a statistical anomaly: the calculated mean is wildly inaccurate, sometimes even returning negative numbers for datasets that contain mostly positive values. A developer suspects that a recent "memory optimization" commit introduced a signed integer overflow during the decoding or aggregation process.

Your objectives:
1. **Secret Recovery**: The client provided a sample dataset at `/app/telemparser/testdata/samples.bin.enc`, but it is encrypted using AES-256-GCM. The hex-encoded decryption key was accidentally committed to the `telemparser` Git repository at some point in the past, and later removed. You must perform Git history forensics to recover this key to test your code.
2. **Troubleshooting**: Investigate the encoding/serialization and aggregation logic in `/app/telemparser` to find the root cause of the statistical anomaly.
3. **Bug Fix**: Fix the bug in the `telemparser` package so that it correctly calculates the mean without overflowing, even for large datasets.
4. **Integration**: Create a Go command-line tool at `/home/user/workspace/statstool/main.go` that imports and uses the `telemparser` package. 
   - It must accept exactly two command-line arguments: `<path-to-encrypted-file>` and `<hex-encoded-key>`.
   - It must print *only* the calculated mean as a floating-point number to standard output.
5. **Regression Test**: Write a regression test in `/app/telemparser/parser_test.go` that specifically catches the integer overflow bug.

Your final submission will be verified by compiling your `statstool` program and running it against a large, held-out dataset. The printed mean must be extremely accurate.

**Note**: Ensure your `statstool` module is properly initialized and can import the vendored package (e.g., using a `replace` directive in your `go.mod` to point to `/app/telemparser`).
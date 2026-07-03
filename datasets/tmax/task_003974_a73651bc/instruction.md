We are trying to set up an automated data cleaning pipeline for our sensor network, but our internal anomaly detection and dimensionality reduction library is behaving strangely. Instead of extracting the main signal and identifying outliers via Bayesian inference, it seems to be keeping the noise and throwing away the signal.

We have provided the source code for this library, `github.com/ds-tools/gonomaly` (version 1.0.0), vendored at `/app/gonomaly-1.0.0`. 

Your tasks are as follows:
1. **Fix the Library**: Inspect the vendored package at `/app/gonomaly-1.0.0`. There is a mathematical/logical bug in `pca.go` affecting the dimensionality reduction step (specifically, how principal components are selected). Fix the bug so that it correctly selects the most important features (highest variance).
2. **Build a Service**: Write a Go application at `/home/user/pipeline/main.go` that imports this fixed library (you may need to set up a `go.mod` with a `replace` directive pointing to `/app/gonomaly-1.0.0`). 
3. **Multi-Protocol Endpoints**:
   - Your application must run a TCP server on port `8081`. When it receives the exact string `STATUS auth_token=secret_123\n`, it must respond with `OK\n` and close the connection.
   - Your application must run an HTTP server on port `8080`.
   - The HTTP server must expose a `POST /clean` endpoint. It will receive a JSON payload with the schema: `{"data": [[float64]]}` (an array of float64 arrays representing numerical records).
   - For each request, parse the data, pass it through the `gonomaly.CleanDataset(data, 2, 0.95)` function (which reduces data to 2 dimensions and filters out anomalies using a 95% Bayesian confidence threshold). The function returns a filtered `[][]float64` slice.
   - Return the filtered dataset as JSON: `{"cleaned_data": [[float64]]}`.

Please write the code, compile it, and run the service in the background so it is actively listening on ports 8080 and 8081. Ensure your solution passes numerical accuracy tests by correctly filtering the anomalies once the bug is fixed.
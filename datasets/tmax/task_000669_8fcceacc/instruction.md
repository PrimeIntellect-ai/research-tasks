You are the on-call engineer, and you just got paged at 3:00 AM. 

Our hybrid data ingestion pipeline is failing. The pipeline consists of a Go service that concurrently fetches financial data and a Python script that aggregates the results. Both have critical bugs that are causing cascading failures in production:

1. **Go Service (Goroutine Leak):** 
The Go fetcher (`/home/user/pipeline/fetcher.go`) is leaking goroutines when the incoming request is cancelled or times out. The unbuffered channel mechanism is flawed, causing worker goroutines to block forever if the parent function exits early due to context cancellation.

2. **Python Service (Precision Loss):**
The Python aggregator (`/home/user/pipeline/aggregator.py`) sums up incoming price ticks. However, it's using standard floating-point arithmetic. With thousands of small fractional values, precision loss is causing a mismatch in our ledgers (e.g., adding `0.1` ten times results in `0.9999999999999999` instead of exactly `1.0`).

**Your objective:**
1. Fix `/home/user/pipeline/fetcher.go` so it no longer leaks goroutines under cancellation. You must not change the function signature: `func FetchData(ctx context.Context, urls []string) []string`.
2. Fix `/home/user/pipeline/aggregator.py` so it precisely sums the inputs without floating-point precision loss. The function signature `def aggregate_prices(prices: list[float]) -> str:` must be preserved, and it must return the exact sum as a string formatted to 2 decimal places. Use the `decimal` module.
3. Once you have fixed both files, write a bash script at `/home/user/pipeline/regression_test.sh` that:
   - Runs `go test` in the `/home/user/pipeline/` directory.
   - Runs `python3 -m unittest test_aggregator.py` in the same directory.
   - Exits with code 0 only if both tests pass. Make sure the script is executable.

The test files `/home/user/pipeline/fetcher_test.go` and `/home/user/pipeline/test_aggregator.py` are already provided and currently fail. Do not modify the test files.
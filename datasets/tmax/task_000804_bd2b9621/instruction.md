You are tasked with building a configuration management tracker that processes time-series logs of server configuration changes, imputes missing data, and prepares it for ingestion. 

A stream of raw configuration updates is available locally, but you must write a robust, reusable Go program that can handle arbitrary inputs of this format via `stdin`.

**Requirements:**
1. **The Tool:** Write a Go program at `/home/user/config_tracker.go` and compile it to `/home/user/tracker`.
2. **Input Format:** Your program must read a stream of JSON Lines (JSONL) from `standard input`. Each line represents a configuration update:
   `{"host": "server-1", "metric": "cpu_limit", "ts": 100, "val": 2.5}`
   * `host` (string): The server identifier.
   * `metric` (string): The configuration parameter name.
   * `ts` (integer): Timestamp in seconds.
   * `val` (float): The configuration value.
3. **Processing & Interpolation:** 
   * Group the data by `host`, then by `metric`.
   * For each group, sort the records by `ts` in ascending order.
   * Resample the time series to a regular 10-second interval grid. The grid must start exactly at the minimum `ts` for that group and end at the highest grid point `T <= maximum ts` for that group.
   * For each grid point `T`:
     * If an exact timestamp `T` exists in the input for that group, use its `val` (if multiple identical `ts` exist, use the last one read).
     * If `T` does not exist, compute `val` using **linear interpolation** between the closest input point before `T` and the closest input point after `T`.
4. **Output Format:** Output the grouped, sorted, and interpolated data to `standard output` as a CSV without a header. The columns must be: `host,metric,ts,val`. Format `val` to exactly 2 decimal places. Order the final output alphabetically by `host`, then alphabetically by `metric`, then chronologically by `ts`.
5. **Vendored Library Issue:** You must parse the JSON using the `github.com/tidwall/gjson` package, which has been pre-vendored on your system at `/app/gjson`. However, the system administrator reported that this specific vendored copy has a bug preventing it from reading floating-point values correctly (it always returns 0 for floats). You must find and fix the deliberate perturbation in the vendored `/app/gjson/gjson.go` file before compiling your code. Set up your `go.mod` to replace `github.com/tidwall/gjson` with the local `/app/gjson` path.

Your program will be rigorously tested against an automated oracle using randomized inputs. Ensure your interpolation math is exact and handles edge cases appropriately.
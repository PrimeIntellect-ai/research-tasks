You are acting as an assistant for a localization engineer who is updating our time-series translation pipeline. 

We have a vendored Go package located at `/app/locales-dag`. This package is responsible for DAG orchestration and pipeline scheduling of translation updates. However, it currently has a broken `Makefile` (it fails to build due to a syntax error where spaces are used instead of tabs for the `build` target) and a minor bug in the scheduling logic where it drops the last item in a time series.

Your task is to:
1. Fix the `Makefile` in `/app/locales-dag` so that running `make` completes successfully.
2. Fix the off-by-one bug in `/app/locales-dag/scheduler.go` so it no longer drops the last item.
3. Write a Go program at `/home/user/transformer.go` and compile it to an executable at `/home/user/transformer`.

The `/home/user/transformer` executable must do the following:
- Read lines from Standard Input (stdin).
- Each line will be formatted as: `<unix_timestamp>,<encoding>,<hex_encoded_payload>`
  Example: `1690000000,iso-8859-1,e963686f`
- The supported encodings are `utf-8`, `iso-8859-1`, and `windows-1252`.
- For each line, decode the hex payload into bytes, then convert those bytes from the specified character encoding into a standard UTF-8 Go string.
- You must use the `/app/locales-dag` package to sort the entries chronologically by their unix timestamp. Assume the package provides a function `dag.SortAndSchedule(entries []dag.Entry) []dag.Entry`. (You can inspect the package to see the exact API).
- Output the sorted results to Standard Output (stdout), one per line, formatted strictly as:
  `<unix_timestamp>|<utf8_string>`

Ensure your compiled program at `/home/user/transformer` is robust, handles malformed hex gracefully by skipping the line, and prints the exact sorted pipeline updates. An automated system will feed randomized translation data into your program and verify that the output perfectly matches a reference implementation.
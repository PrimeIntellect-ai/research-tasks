We are currently triaging a severe incident where our log aggregation pipeline is randomly hanging and occasionally computing incorrect timestamps, causing negative latencies in our monitoring dashboards.

The pipeline relies on a vendored version of the `arrow` library, located at `/app/arrow-1.2.3`. During a recent internal hackathon, someone attempted to add a "custom fast-path parser" to the vendored `arrow` source. Unfortunately, this introduced:
1. An infinite loop when parsing specific timezone formats (causing the pipeline to hang).
2. A numerical bug when extracting fractional seconds, leading to inaccurate intermediate states and query results.

We have a wrapper script `/app/parse_logs.py` that uses this vendored library to parse a log timestamp string and output its normalized UTC epoch representation. We also have a pre-compiled oracle binary `/app/parse_logs_oracle` which contains the correct implementation.

Your task is to:
1. Diagnose and fix the infinite loop in the vendored `arrow` package.
2. Fix the numerical instability / parsing edge-case bug in the vendored package.
3. Ensure that `/app/parse_logs.py "<timestamp_string>"` behaves **exactly** identical to `/app/parse_logs_oracle "<timestamp_string>"` for any valid ISO-8601 or custom timestamp format.

Do not modify `/app/parse_logs.py`. You must apply your fixes directly to the source code of the vendored package in `/app/arrow-1.2.3`. An automated fuzzer will test your wrapper script against the oracle using a wide distribution of edge-case timestamps.
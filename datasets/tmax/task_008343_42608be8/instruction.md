You are an on-call engineer and have just been paged at 3:00 AM. 

The API Gateway is reporting HTTP 500 Internal Server Errors from the Pricing Service for a specific request that consistently fails every time the client retries.

Here is what you know:
- The API Gateway logs are located at `/home/user/logs/gateway.log`.
- The Pricing Service logs are located at `/home/user/logs/pricing.log`.
- A python script at `/home/user/calc_volatility.py` is invoked by the Pricing Service to compute the volatility (standard deviation) of a list of prices.
- The issue seems to be crashing the `calc_volatility.py` script.

Your task:
1. Reconstruct the timeline of the failed request that occurred exactly at `03:00:00` by correlating the logs across the two services.
2. Identify the specific payload that caused the failure. Note that the upstream service occasionally sends payloads in a serialized/encoded format.
3. Diagnose and fix the bug in `/home/user/calc_volatility.py`. The script contains a naive mathematical implementation that suffers from numerical instability (catastrophic cancellation) when processing prices with very small variations, causing it to occasionally calculate a negative variance and crash with a `ValueError: math domain error`.
4. Fix the script so it computes the volatility robustly.
5. Manually decode the payload from the failed 03:00:00 request, pass the decoded comma-separated string of prices to your fixed script, and save the script's exact output to a file named `/home/user/solution.txt`.
You are the on-call engineer and you just got a 3 AM PagerDuty alert. The production `yield-calculator` service is crash-looping. 

Here is what we know:
1. The container logs have been dumped to `/home/user/container_logs.txt`.
2. The service source code is located in a Git repository at `/home/user/yield-calculator`.
3. To run the service or its test suite locally, you need a `VAULT_SECRET` environment variable. The secret was accidentally committed to the repository in the past, but later removed. 

Your tasks:
1. **Log Inspection & Secret Recovery**: Inspect the container logs to identify the panic. Dig through the Git repository's history to find the leaked `VAULT_SECRET`. Write this secret string exactly as found to `/home/user/recovered_secret.txt` (no newlines or extra spaces).
2. **Formula Correction**: The logs indicate a panic related to an arithmetic overflow in `src/lib.rs`. The function `calculate_yield(principal: u64, rate_bps: u64, time_years: u64) -> u64` is implemented incorrectly. The correct financial formula should be: `principal * (10000 + (rate_bps * time_years)) / 10000`. Fix the formula in `src/lib.rs`.
3. **Verification**: Once fixed, the test suite should pass. Run the tests to ensure your fix is correct.
4. **Final Output**: Write the calculated yield for a principal of `500000`, a rate of `450` bps, and a time of `5` years to `/home/user/yield_result.txt`.

Please complete these steps and ensure `/home/user/recovered_secret.txt` and `/home/user/yield_result.txt` are populated correctly.
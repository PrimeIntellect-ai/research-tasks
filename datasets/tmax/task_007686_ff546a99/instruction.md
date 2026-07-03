You are an on-call engineer and you've just received a 3 AM page. The primary background worker container for the trading system (`prod-analyzer-01`) has crashed repeatedly, halting real-time market data processing. 

The previous on-call engineer started investigating but was paged away to another incident. They left you some notes:
- "The container logs are at `/home/user/crash_logs/prod-analyzer-01.log`. Look for the panic to find the specific Transaction ID (`tx_id`) that caused it."
- "I tried to fix the code in `/home/user/trade_analyzer`, but I messed up the `Cargo.toml` dependencies while trying to force a downgrade. The project won't even build right now due to a dependency resolution error."
- "The crash seems to be a formula implementation error in the Volume-Weighted Average Price (VWAP) calculation."

Your objectives are:
1. **Forensics & Log Inspection:** Inspect the container logs to find the exact `tx_id` of the payload that caused the panic.
2. **Dependency Conflict Resolution:** Fix the `Cargo.toml` in `/home/user/trade_analyzer` so that the project compiles. The previous engineer set the `thiserror` crate version to a non-existent/conflicting version. Standardize it to a valid version (e.g., `"1.0"`).
3. **Formula Correction:** Edit `src/vwap.rs`. The `calculate_vwap` function panics due to a division by zero when the total volume of trades is exactly `0`. Update the implementation so that if the total volume is `0`, the function safely returns `0.0` instead of panicking.
4. **Verification:** Ensure that `cargo test` passes in the `/home/user/trade_analyzer` directory.
5. **Reporting:** Create a report file at `/home/user/forensics_report.txt`. 
   - Line 1 must contain exactly the `tx_id` that caused the crash.
   - Line 2 must contain the corrected VWAP output for that transaction when you run the CLI tool: run `cargo run -- --tx <CRASHING_TX_ID>` and put its numerical output on line 2.

Everything you need is located in `/home/user/trade_analyzer` and `/home/user/crash_logs/`.
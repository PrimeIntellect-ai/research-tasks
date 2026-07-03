You have inherited a legacy Rust application from a departed developer. The application has two immediate problems that require your attention:

1. **Forensic Recovery**: The application crashed in production yesterday, leaving behind a partial memory dump. The system requires an active session token to restart the recovery process, but the original logs were lost. The token is known to follow the exact format `SESSION_TOKEN:<32-character lowercase hex string>`.
   Analyze the provided memory dump located at `/home/user/forensics/memory.dmp`. Extract the token and write the exact, complete 32-character hex string (without the `SESSION_TOKEN:` prefix) to a new file at `/home/user/solution/token.txt`.

2. **Intermittent Failure Resolution**: The codebase located in `/home/user/legacy_app` contains a function `get_priority_worker` in `src/lib.rs`. There is an intermittent test failure that causes a panic in production. The developer's notes say: "Sometimes it panics when multiple workers have the exact same score. It seems random."
   Investigate the codebase. You will find that the intermittent failure is caused by Rust's randomized `HashMap` iteration order when breaking ties. 
   Fix the `get_priority_worker` function so that it behaves deterministically: if multiple workers have the exact same highest score, the tie MUST be broken by selecting the worker whose name comes first alphabetically.

Your final state will be verified by:
- Checking the contents of `/home/user/solution/token.txt`.
- Running `cargo test` in `/home/user/legacy_app` repeatedly to ensure the intermittent panic is entirely resolved and the logic is correct.
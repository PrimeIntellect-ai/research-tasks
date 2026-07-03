You are an application security engineer. Your team uses a custom serialized data format called "Secure Web Payload" (SWP) for internal microservices. To prevent injection attacks, payloads are processed through a strict state machine parser.

Recently, the team tried to rewrite the parser in Rust for performance, but the project (`/home/user/rust_parser/`) fails to compile due to complex lifetime issues across its multiple files (`main.rs`, `parser.rs`, `state.rs`). 

Since the microservice rollout is blocked, your task is to translate the intended logic from the broken Rust project into a working Python script.

Requirements:
1. Examine the broken Rust code in `/home/user/rust_parser/` to understand the state machine transitions, serialization format, and security rules.
2. Write a Python script at `/home/user/parser.py` that implements the exact same state machine and parsing logic.
3. The parser must accept a single command-line argument: the path to a `.swp` file.
4. The SWP format starts with a version header (e.g., `VERSION v1.2.3`). Your Python script must perform semantic version comparison. It should only accept payloads where `1.2.0 <= version < 2.0.0`. If the version is out of bounds, print exactly `INVALID_VERSION` and exit.
5. Next is a `SIZE N` header (where N is the number of transition lines).
6. The remaining N lines are state machine actions in the format `ACTION:data`. 
7. The state machine always starts in the `INIT` state. If an `EVAL` action is attempted while the state is not `SAFE`, the parser must detect this web security violation, print exactly `REJECTED_INJECTION`, and exit.
8. If an invalid action or transition occurs, print exactly `INVALID_STATE` and exit.
9. If all actions are processed successfully and the machine reaches the `ACCEPT` state, print exactly `VALID`. If it ends in any other state, print `INVALID_STATE`.
10. Finally, there is a directory of test payloads at `/home/user/payloads/`. Create a bash script at `/home/user/run_all.sh` that runs your `parser.py` on every `.swp` file in the directory (in alphabetical order) and appends the output to `/home/user/results.log` in the format: `<filename>: <RESULT>`.

Example line in `/home/user/results.log`:
`payload_1.swp: VALID`
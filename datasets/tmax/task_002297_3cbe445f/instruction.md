I am organizing my project files and found an execution log file at `/home/user/transitions.log` representing the trace of a mathematical state machine. I need to test if the state machine followed a valid continuous path and what its final mathematical score was.

Please write a Rust program at `/home/user/evaluate.rs` that implements a parser and state machine simulator to process this log. 

The log contains various debug and info lines, but the state transitions we care about always start with the exact string `[SEQ]`.
The format of a transition line is:
`[SEQ] State: <CurrentState> Action: <ActionName> Weight: <Integer> Next: <NextState>`

Your Rust program must do the following:
1. Initialize the state machine at the state `"START"` with a total score of `0`.
2. Read `/home/user/transitions.log` sequentially line by line.
3. Ignore any line that does not begin with `[SEQ]`.
4. For lines beginning with `[SEQ]`, parse the `<CurrentState>`, `<Integer>` (which can be negative), and `<NextState>`.
5. If the parsed `<CurrentState>` exactly matches the machine's current state, add the `<Integer>` weight to the total score, and update the current state to `<NextState>`.
6. If the parsed `<CurrentState>` does NOT match the machine's current state, you have encountered a discontinuity. You must immediately halt processing the log (do not process any further lines).
7. Write the final state and the final score to `/home/user/summary.json` in the following exact JSON format:
`{"final_state": "STATE_NAME", "score": 123}`

Once you have written the Rust program, compile it using `rustc` and run it so that the `/home/user/summary.json` file is successfully generated.
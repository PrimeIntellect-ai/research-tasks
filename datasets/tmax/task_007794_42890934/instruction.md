I am a web developer building a new conversion-tracking feature for our e-commerce site. I need to parse a high-volume event log to find users who successfully completed a specific "user journey" funnel. 

We have a log file located at `/home/user/events.log`. Each line represents an event in the format `USER_ID,EVENT_TYPE` (comma-separated). The events are chronologically ordered.

The possible event types are `LOGIN`, `VIEW_ITEM`, `ADD_CART`, `CHECKOUT`, and `LOGOUT`.

You need to write a Go program at `/home/user/journey.go` that implements a state machine to track each user's progress through the conversion funnel. 
The funnel consists of these exact steps in order:
1. `LOGIN`
2. `VIEW_ITEM`
3. `ADD_CART`
4. `CHECKOUT`

Rules for the state machine:
- A user starts outside the funnel.
- `LOGIN` moves the user to step 1.
- `VIEW_ITEM` moves the user to step 2 ONLY IF they are currently at step 1.
- `ADD_CART` moves the user to step 3 ONLY IF they are currently at step 2.
- `CHECKOUT` moves the user to step 4 ONLY IF they are currently at step 3. Once at step 4, the user is considered to have "completed" the funnel.
- `LOGOUT` immediately resets the user's progress back to the start (outside the funnel), regardless of their current step.
- Any other out-of-sequence events (e.g., a `VIEW_ITEM` while at step 2) are ignored and do not change the state.

Your tasks:
1. Initialize a Go module named `webfeature` in `/home/user/`.
2. Write `/home/user/journey.go`. The program must read `/home/user/events.log`. Since the real log will be massive, you must use Go concurrency (e.g., goroutines and channels) to process the users' state machines in parallel. 
3. The program should output a list of the `USER_ID`s that successfully completed the funnel (reached step 4) to a file named `/home/user/completed_users.txt`. The IDs must be written one per line, sorted alphabetically.
4. Write a benchmark test in `/home/user/journey_test.go` that benchmarks your parsing and state machine logic using Go's `testing` package.
5. Run the benchmark using `go test -bench .` and redirect the output to `/home/user/bench.txt`.
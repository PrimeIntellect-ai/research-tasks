You are an IT support technician acting as a Level 3 escalation engineer. We have a ticket regarding intermittent data corruption in our Python-based distributed message processor.

The system has two components: a Producer and a Consumer. Lately, some messages are being processed with incorrect internal sequence counters.

Here is your task:

**Phase 1: Log Timeline Reconstruction**
Analyze the logs in `/home/user/ticket_data/producer.log` and `/home/user/ticket_data/consumer.log`. 
Reconstruct the timeline to find the single message ID where the "expected_sequence" logged by the Producer does not match the "actual_sequence" logged by the Consumer. 
Write ONLY the corrupted message ID (e.g., `MSG_1234`) to `/home/user/corrupted_id.txt`.

**Phase 2: Fuzzing and Git Bisection**
The source code for the consumer is located in the Git repository at `/home/user/message_processor/`. 
The bug is known to be a race condition introduced recently. 
1. Write a Python fuzzing script (`/home/user/fuzz_test.py`) that concurrently sends 1000 requests to the `process_messages()` function in `processor.py` using `asyncio.gather`. 
2. The function should return a sequence of 1000 unique integers. If the length of the set of returned integers is less than 1000, the race condition has occurred.
3. Use your fuzzer to perform a `git bisect` to find the exact commit that introduced the race condition. The `main` branch is bad, and the tag `v1.0` is good.
4. Write the full 40-character commit hash of the bad commit to `/home/user/bad_commit.txt`.

**Phase 3: Race Condition Debugging & Fixing**
Once you have identified the offending commit, check out the `main` branch again.
Modify `/home/user/message_processor/processor.py` to fix the race condition. You must ensure thread-safe/async-safe operations on the shared state (hint: use `asyncio.Lock()`).

*Deliverables to verify:*
1. `/home/user/corrupted_id.txt` contains the corrupted message ID.
2. `/home/user/bad_commit.txt` contains the bad commit hash.
3. The modified `/home/user/message_processor/processor.py` must be free of race conditions when tested concurrently.
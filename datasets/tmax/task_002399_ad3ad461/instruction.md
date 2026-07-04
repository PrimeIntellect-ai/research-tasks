Wake up, you've just been paged at 3:00 AM. 

The billing team is reporting that our daily revenue aggregation system is occasionally under-reporting totals. They’ve noticed that when processing high volumes of concurrent transactions, the final aggregated numbers don't match the sum of the raw inputs. 

The application code is located at `/home/user/app/event_processor.py`. It uses a custom `Aggregator` class to process batches of JSON events across multiple threads.

Your tasks to resolve this incident:
1. **Comprehend and Fix**: Analyze `/home/user/app/event_processor.py`, identify the concurrency bug (race condition) causing the dropped counts, and fix it directly in the file. Ensure the logic remains thread-safe while preserving the existing method signatures.
2. **Fuzz Testing**: Write a script at `/home/user/fuzz_test.py` that generates large, randomized batches of events (fuzzing) and feeds them into `run_batch`. It should independently calculate the expected total, compare it against the `run_batch` output, and exit with code 0 if they match, or code 1 if they mismatch. (It should consistently pass against your fixed code).
3. **MRE Creation**: The core team wants a Minimal Reproducible Example for their post-mortem. Create `/home/user/mre.py` containing less than 35 lines of code. It should import the `Aggregator` from the (buggy version of) `event_processor`, and demonstrate the data loss simply and consistently without needing JSON parsing or complex thread pools (just raw threading or simpler constructs). 
4. **Incident Report**: Write a brief file at `/home/user/incident_report.txt` containing exactly the name of the standard library concurrency primitive you used to fix the bug (e.g., `Semaphore`, `Lock`, `RLock`, `Condition`, `Event`, etc.) on a single line.

Ensure all python scripts you write are executable or runnable via `python3 <script>`.
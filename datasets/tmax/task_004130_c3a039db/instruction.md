Hey, I'm an IT support technician currently escalating a P1 ticket, and I need your help. 

Our logging pipeline is currently down. The system relies on a multithreaded C++ log aggregator to reconstruct timelines across three different microservices. However, the current version of the source code (`/home/user/buggy_aggregator.cpp`) is deadlocking under high contention and is outputting the wrong timestamp format.

We have a compiled stripped binary of an older, working version (`/app/oracle_bin`), but its source code was lost. We also have a screenshot attached to the original Jira ticket from the developer (`/app/ticket_screenshot.png`) which contains handwritten notes specifying the exact string format the parsed logs need to be converted to.

Your task is to:
1. Examine `/home/user/buggy_aggregator.cpp` to identify and resolve the multithreading deadlocks (race conditions/circular mutex locks).
2. Extract the correct output format string from the image `/app/ticket_screenshot.png` using OCR (e.g., `tesseract`) or visual inspection.
3. Update the C++ code to apply this exact formatting to the log reconstruction output.
4. Compile your fixed C++ program and save the executable exactly at `/home/user/fixed_aggregator`.

The resulting binary must read raw logs from `stdin` and print the formatted logs to `stdout`. Its behavior and output must be **bit-for-bit identical** to `/app/oracle_bin` for any given sequence of standard inputs. We will be fuzz-testing your compiled binary against the oracle with thousands of randomized input log sequences.
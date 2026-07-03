You are an on-call engineer and you've just been paged at 3 AM. The backend transaction processing system has completely frozen under high load.

You have been provided the faulty script at `/home/user/transaction_processor.py`. The script simulates concurrent transfers between user accounts. Under high contention, it deadlocks and never completes.

Your task is to:
1. Analyze `/home/user/transaction_processor.py` to understand why the threads are deadlocking.
2. Fix the concurrency bug in the `transfer` function so that deadlocks are mathematically impossible, without removing the concurrent nature of the processing (do not use a single global lock for all transfers).
3. Ensure the script runs to completion.

When the fixed script successfully completes, it will automatically compute the sum of all account balances and write it to `/home/user/success.log`. 

Please fix the file and run it so that `/home/user/success.log` is generated with the correct final state. Do not modify the `main` function or the number of threads/iterations.
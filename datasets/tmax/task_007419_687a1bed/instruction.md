Wake up! It's 3 AM and you've just been paged. Our financial processing pipeline is intermittently producing incorrect daily aggregates, and customers are complaining about missing funds in their reports. 

The issue has been isolated to a multi-threaded C program that performs mathematical aggregation (summing squares of transactions from multiple regional data files). It usually works, but under high load, the final total is sometimes less than it should be.

The codebase is located at `/home/user/app/aggregator.c`.
The regional data files are located at `/home/user/app/data/region1.txt` through `/home/user/app/data/region4.txt`.

Your task:
1. Diagnose and fix the intermittent failure in `/home/user/app/aggregator.c`. The program spawns a thread for each region file, calculates the sum of squares of the integers in that file, and adds it to a global `total_sum`.
2. Recompile the fixed code to `/home/user/app/aggregator_fixed` using `gcc -pthread -o aggregator_fixed aggregator.c`.
3. Verify that running `/home/user/app/aggregator_fixed` produces the correct mathematical result consistently, without any race conditions.
4. Write the final, consistently correct aggregate value (just the numeric output) to `/home/user/app/resolution.txt`.

Ensure your fix does not change the core mathematical logic (sum of squares), but strictly resolves the concurrency bug.
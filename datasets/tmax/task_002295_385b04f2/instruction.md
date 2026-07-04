You are an engineer investigating a critical issue in our long-running financial service, `finance-aggregator`. Recently, the service has been running out of memory (OOM) after a few hours of processing. Furthermore, our QA team reported that the aggregated trade totals are suffering from precision loss and non-deterministic results, suggesting a concurrency bug.

The source code for the service is vendored on the system at `/app/finance-aggregator-1.0`. 

However, we can't even compile the latest version of the code right now. A junior developer added a new source file with a space in the filename, and the custom build script (`build.sh`) now fails with obscure errors.

Your objectives:
1. Diagnose and fix the build failure in `/app/finance-aggregator-1.0/build.sh`.
2. Find and fix the memory leak in the C++ source code.
3. Find and fix the race condition causing incorrect/non-deterministic trade totals. 
4. Once fixed, compile the code and copy the working binary to `/home/user/finance-aggregator-fixed`.

To test your fix, you can run your compiled binary against the mock data in `/home/user/mock_data/` (which contains several data files, some with spaces in their names). 

Ensure your final binary efficiently processes all data without excessive memory consumption and correctly sums the trade values. An automated verification script will run your binary against a massive dataset, measuring its maximum memory footprint and output accuracy.
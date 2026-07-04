You are an on-call engineer who just received a 3 AM page. A critical mathematical aggregation service running in a container is periodically locking up and timing out under high contention, bringing down the downstream reporting pipeline. 

You have extracted the problematic container's latest error logs to `/home/user/container_logs.txt` and the batch of queries it was processing to `/home/user/queries.txt`. 

The source code for the running service is located at `/home/user/processor.go`. 

Your initial diagnosis indicates that the service is experiencing an infinite loop (livelock) due to floating-point precision loss during an accumulation sequence for specific query targets. The developer used an inadequate data type for accumulating very small steps to reach large target values.

Your task:
1. Identify which query in `/home/user/queries.txt` is causing the livelock (you may use delta debugging or inspect the logs to isolate it).
2. Fix the source code in `/home/user/processor.go` to eliminate the precision loss livelock (ensure the accumulator and step use standard 64-bit precision).
3. Recompile the code (`go build -o processor processor.go`).
4. Run the fixed binary on the input file: `./processor /home/user/queries.txt`
5. Save the exact, complete standard output of your successful run to `/home/user/results.txt`.

Everything you need is in the `/home/user` directory.
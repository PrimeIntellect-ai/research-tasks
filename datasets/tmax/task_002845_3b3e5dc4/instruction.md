You are a log analyst investigating traffic patterns between two redundant servers, Alpha and Beta. The servers are supposed to receive identical traffic, but due to load balancer glitches, their request counts have diverged. 

You have two log files:
1. `/home/user/server_alpha.log`
2. `/home/user/server_beta.log`

The logs contain entries formatted like this:
`[EPOCH_TIMESTAMP] host=hostname reqs=REQUEST_COUNT`

Example:
`[1700000000] host=alpha reqs=5`

However, the logging system only writes a line if there were requests during that second. If a server received 0 requests in a given second, there is no log line for that timestamp.

Your objective is to quantify the divergence between the two servers by calculating the Manhattan distance (sum of absolute differences) between their request counts over the exact same time window.

To do this, you must:
1. Parse the timestamps and request counts from both logs.
2. Determine the global minimum timestamp and global maximum timestamp across BOTH logs combined. This defines your continuous time window.
3. Resample and gap-fill the data: Create an aligned, continuous timeline from the global minimum to the global maximum timestamp (inclusive) at 1-second intervals. If a server has no log entry for a specific second, assume its request count for that second is 0.
4. Calculate the absolute difference in request counts between Alpha and Beta for every single second in the continuous timeline.
5. Sum these absolute differences to get the total Manhattan distance.

Finally, write the total sum to a file named `/home/user/distance_result.txt` in the following exact format:
`Total Distance: <integer_value>`

You may use any language or standard CLI tools available in the environment to solve this.
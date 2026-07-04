You are an IT support technician responding to an escalated ticket. 

**Ticket #9942: Legacy filter tool crashing on new logs**
"Our legacy log filtering tool, `legacy_filter`, has started crashing intermittently on our new production logs. We also recently migrated to a new container environment, and the tool currently won't even execute (giving some kind of permission or format error). 

We need you to:
1. Fix the environment/binary so `legacy_filter` can run. It is located at `/app/legacy_filter`.
2. Fuzz or test the binary to reproduce the intermittent crashes. The crashes seem to happen based on specific log line lengths or formats.
3. Debug the output to deduce the exact filtering logic the binary is applying. It takes a column index (1-based) and a file path: `/app/legacy_filter <column_index> <input_file>`.
4. Write a robust replacement script in Python at `/home/user/robust_filter.py`. It must accept the same arguments (`python3 robust_filter.py <column_index> <input_file>`) and output the exact same lines as the original tool would if it didn't crash. 

Your Python script must perfectly replicate the logical filtering condition of the binary but gracefully handle the edge cases that cause the C binary to overflow/crash. Print the matching lines to standard output. 

Ensure your `/home/user/robust_filter.py` script is executable and prints the correct subset of lines from the input file. We will test your script against a hidden dataset of logs."
You are a data engineer building ETL pipelines. You have a raw log file located at `/home/user/pipeline.log` which contains various system logs, but also records the directed dependencies between pipeline stages in the format:
`[DEPENDENCY] source_stage -> dest_stage`

You need to identify the pipeline stage that has the highest out-degree (i.e., the stage that acts as a source for the most destination stages). This is a simple measure of out-degree centrality for our pipeline graph.

To do this, complete the following steps:
1. Write a C program located at `/home/user/max_degree.c` that reads a sorted list of source node names from standard input (one name per line) and calculates the frequencies of each node to find the one with the highest count. It must print the result to standard output in exactly this format: `MAX_NODE=<stage_name> COUNT=<count>`. If there is a tie, output the first one encountered.
2. Compile your C program to an executable named `/home/user/max_degree`.
3. Construct a shell pipeline that uses standard Bash/Unix tools (e.g., `grep`, `awk`, `sort`) to extract ONLY the `source_stage` names from the `[DEPENDENCY]` lines in `/home/user/pipeline.log`, sorts them, and pipes them into your `/home/user/max_degree` executable.
4. Redirect the final output of your pipeline to a file named `/home/user/result.txt`.

Ensure your C program is robust enough to handle string lines up to 255 characters long and properly detects the end of standard input.
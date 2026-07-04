You are a data engineer troubleshooting a complex ETL pipeline. A recent deployment introduced a bottleneck, and we suspect some jobs are waiting on distant dependencies that act like deadlocks under heavy concurrent load. 

To help analyze the pipeline's execution plan, we need a tool to traverse the dependency graph and compute the shortest execution path between any two ETL jobs.

In `/home/user/etl_dependencies.csv`, you will find the schema of our pipeline dependencies. The file has no header and contains comma-separated values in the format:
`upstream_job_id,downstream_job_id`
(This means `upstream_job_id` must complete before `downstream_job_id` can start).

Your task:
Write a Bash script at `/home/user/analyze_deps.sh` that takes exactly two arguments: a `start_job` and an `end_job`. 
The script must project this CSV into a graph, find the shortest path from `start_job` to `end_job`, and print the path to standard output. 
The output format must be the job names separated by `->`. If there are multiple paths of the same shortest length, any of them is acceptable.

Example usage:
`/home/user/analyze_deps.sh extract_users aggregate_metrics`

Example output:
`extract_users->transform_users->load_users->aggregate_metrics`

You may use standard Linux tools or inline a Python/Perl/Ruby script within your Bash wrapper to handle the graph traversal, provided the main entry point is the Bash script `/home/user/analyze_deps.sh`. Make sure the script is executable.

After creating and testing your script, run it with the arguments `extract_users` and `report_generation`, and save the output to `/home/user/critical_path.txt`.
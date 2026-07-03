As a Database Reliability Engineer (DBRE), you are responsible for optimizing our nightly database backup schedules. The backup jobs have strict dependencies on one another to ensure data consistency, forming a Directed Acyclic Graph (DAG) of jobs. 

You have been provided with a plain text file at `/home/user/backup_dependencies.txt`. Each line contains two job names separated by a single space (`UpstreamJob DownstreamJob`), indicating that `UpstreamJob` must complete successfully before `DownstreamJob` can begin. The file contains jobs from various environments (`prod-`, `dev-`, `staging-`).

Using only standard Linux Bash utilities (like `awk`, `grep`, `sort`, `join`, `uniq`, etc.), perform the following graph analytics tasks:

1. **Graph Projection**: Filter the dataset to isolate the production graph. You should only consider edges where *both* the upstream and downstream jobs start with the prefix `prod-`. 

2. **Graph Analytics (Centrality)**: In this `prod-` subgraph, determine which backup job is the most critical upstream dependency. Find the job with the highest out-degree (the highest number of immediate downstream dependencies). Write the name of this single job to `/home/user/highest_outdegree.txt`. If there is a tie, output the one that comes first alphabetically.

3. **Knowledge Graph Pattern Matching**: Find all sequences of exactly 3 dependent jobs (e.g., Job A -> Job B -> Job C) within the `prod-` subgraph. Write these paths to `/home/user/backup_chains.txt`.
   - The format must be exactly: `JobA,JobB,JobC`
   - The file must be sorted alphabetically.

Ensure your final outputs exactly match the requested formats, as they will be automatically evaluated. Do not include any extra text or headers in the output files.
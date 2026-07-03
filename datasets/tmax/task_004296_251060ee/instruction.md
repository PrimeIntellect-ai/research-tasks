You are a database reliability engineer tasked with migrating away from a proprietary backup management tool. 

The old system uses a closed-source, stripped binary located at `/app/backup_router`. This tool calculates the replication dependency chain length (shortest path) between two database instances by reading a daily backup topology log.

Your goal is to reverse-engineer the data model used by this proprietary tool and write a completely open-source replacement script in Bash (using only standard shell utilities like `awk`, `grep`, `sed`, `bash`).

The topology log files contain sequential entries representing database backup events and their dependencies. You need to figure out exactly how the binary interprets this file to build a directed graph, and how it calculates the path length between a source and a target node. 

Create a script at `/home/user/route.sh` that takes exactly three arguments:
1. The path to a topology log file
2. The source database ID
3. The target database ID

Your script must output exactly what the `/app/backup_router` binary outputs for the same inputs (the shortest path distance as an integer, or the specific unreachable message it uses).

You can use the `/app/backup_router` binary as a black-box oracle to test your assumptions about the data model, graph traversal direction, and output format. You can create dummy log files to feed into the binary to observe its behavior. 

Your final script will be tested against the proprietary binary using a fuzzing verifier that generates dozens of random topology logs and queries. Your script's output must perfectly match the binary's output for all test cases. Ensure your script is executable (`chmod +x`).
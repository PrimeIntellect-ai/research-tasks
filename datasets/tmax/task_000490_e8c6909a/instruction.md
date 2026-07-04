You are helping a researcher organize their data pipelines. They have an SQLite database located at `/home/user/datasets.db` containing metadata about their datasets and how they depend on each other to build. 

Recently, the build system has been hanging due to what looks like "transaction deadlocks" in the data pipeline. We suspect this is caused by circular dependencies between datasets.

Your task is to:
1. Reverse engineer the schema of `/home/user/datasets.db` to understand how datasets and their dependencies are stored.
2. Write a single bash script at `/home/user/find_deadlocks.sh` that queries this database using the `sqlite3` CLI tool.
3. The script must find all pairs of datasets that have a **direct mutual dependency** (Dataset A depends on Dataset B, AND Dataset B depends on Dataset A).
4. For each mutual dependency pair, calculate their "combined in-degree centrality"—the total number of dependencies pointing to *either* dataset in the pair from anywhere in the network (including the dependencies they have on each other).
5. The script should output the results directly to standard output (stdout) in the following format:
   `DatasetName1,DatasetName2,CombinedInDegree`
6. Ensure that for each pair, `DatasetName1` comes alphabetically before `DatasetName2`. Sort the final output lines alphabetically by `DatasetName1`.

Make sure your script is executable and prints exactly the required CSV output and nothing else.
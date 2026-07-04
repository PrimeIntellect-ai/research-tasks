You are a data engineer building a custom ETL pipeline execution engine. The engine occasionally freezes due to cyclic dependencies (deadlocks) in the task definition graph.

You have exported the task dependency schemas from your NoSQL database using an aggregation pipeline. The export is available at `/home/user/pipeline_export.csv`. 

The file has a variable number of columns per row. The format is:
`task_id,status,dependency_1,dependency_2,...`

Your task is to write a C program that analyzes these relationships and identifies all deadlocks.

Requirements:
1. Write a C program at `/home/user/detect_cycles.c`.
2. The program must read `/home/user/pipeline_export.csv`.
3. Filter out any task where `status` is `inactive`. An inactive task should not be included in the graph, and any dependencies pointing to it or from it should be ignored.
4. Model the active tasks and their dependencies as a directed graph. A dependency means `task_id` -> `dependency_x`.
5. Detect all simple cycles (deadlocks) in the graph. You can assume that for this specific dataset, cycles are disjoint (no task belongs to more than one cycle).
6. The program must output the detected cycles to `/home/user/deadlocks.out`.
7. **Output Formatting:** 
    - Each line in `/home/user/deadlocks.out` must represent exactly one cycle.
    - The task IDs within a single cycle must be sorted alphabetically and separated by commas (e.g., `JobA,JobB,JobC`).
    - The lines in the file must also be sorted alphabetically based on the first task ID of each line.

Compile your C program using `gcc /home/user/detect_cycles.c -o /home/user/detect_cycles` and run it to produce the `deadlocks.out` file.
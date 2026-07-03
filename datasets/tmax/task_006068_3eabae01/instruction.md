You are acting as a Database Administrator optimizing a custom graph processing pipeline. We have a C program that projects a bipartite graph (Users and Products) into a User-User network (where an edge exists if two users bought the same product) and computes the degree centrality (number of shared connections) for each user.

However, the current C program (`/home/user/project_graph.c`) has a critical bug. It is producing massive, incorrect degree counts because of a logical error in the projection step that acts like an "implicit cross join" in SQL, connecting users unconditionally or incorrectly.

Your task:
1. Inspect and fix the bug in `/home/user/project_graph.c`. The program should correctly count how many *other* users share at least one product with a given user. (Do not count the user themselves).
2. Compile the fixed program to an executable named `/home/user/project_graph`.
3. Run it against the input dataset located at `/home/user/bipartite.txt`.
4. The program prints `UserID,Degree` to standard output. Use shell commands to chain this output, sort it to find the single UserID with the highest degree centrality, and write ONLY that UserID (as an integer) to `/home/user/top_user.txt`. In case of a tie, write the numerically smallest UserID.

Ensure all files are exactly where specified.
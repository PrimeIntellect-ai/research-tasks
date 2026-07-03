You are an AI assistant helping a research scientist analyze a network of academic collaborations. The researcher has provided you with two CSV datasets representing a graph of authors and their co-authorships. They need a quick command-line tool to analyze the "2nd-degree" professional network of specific authors to understand interdisciplinary reach.

**Dataset Schema:**
You have two files located in `/home/user/`:
1. `/home/user/authors.csv`
   Format: `AuthorID,Name,Department,YearJoined`
   (Note: No header row, purely data)

2. `/home/user/coauthors.csv`
   Format: `Author1_ID,Author2_ID,PublicationCount`
   (Note: No header row. Edges are undirected, meaning if Author A co-authored with Author B, the row might appear as `A,B,Count` OR `B,A,Count`. They will not appear twice.)

**Your Task:**
Create a Bash script at `/home/user/analyze_collaboration.sh` that takes exactly one argument: the `AuthorID` of a target author.

The script must perform the following graph traversal and aggregation operations entirely using standard Unix text-processing tools (like `awk`, `grep`, `sed`, `sort`, `join`, etc.):
1. Identify all 1st-degree connections (authors who have co-authored directly with the target author).
2. Identify all 2nd-degree connections (authors who have co-authored with the 1st-degree connections).
3. Filter the 2nd-degree connections to **strictly exclude** the target author themselves and any 1st-degree connections. (We only want exactly 2-hop connections).
4. Map these strict 2nd-degree connection IDs back to their respective `Department` using `authors.csv`.
5. Aggregate and count the number of 2nd-degree connections in each department.
6. Print the result to Standard Output in the format: `DepartmentName:Count`, with the output sorted alphabetically by `DepartmentName`.

**Example:**
If Author 10 is in the Physics department, co-authored with Author 11 (Math), and Author 11 co-authored with Author 12 (Biology) and Author 13 (Biology) - assuming no other links - running `./analyze_collaboration.sh 10` should output:
```
Biology:2
```

Ensure your script has execution permissions (`chmod +x`). The automated test will invoke your script with a specific AuthorID and check the standard output.
You are an assistant helping a researcher organize their dataset of academic publications.

The researcher has exported their relational database into two CSV files located in `/home/user/`:
1. `/home/user/researchers.csv` - Contains researcher identities.
   Format: `id,name`
2. `/home/user/authorship.csv` - Contains the relationships between researchers and the papers they have authored.
   Format: `researcher_id,paper_id`

The researcher needs a tool to query the co-authors of a given researcher. Previously, they tried writing a SQL query for this, but it accidentally produced an implicit cross join, returning every researcher paired with every other researcher instead of actual co-authors.

Your task is to write a standard C++ program (without relying on external libraries like Boost or nlohmann/json; use standard `<iostream>`, `<fstream>`, `<string>`, `<vector>`, etc.) to correctly perform this knowledge graph pattern matching.

Requirements:
1. Create a C++ source file at `/home/user/coauthor_query.cpp`.
2. The program must accept exactly one command-line argument: the name of the target researcher (e.g., `./coauthor_query "Dr. Alice Smith"`).
3. The program must parse the CSV files and map the relational data to find all unique co-authors of the target researcher. A co-author is anyone who shares at least one `paper_id` with the target researcher.
4. The program must NOT include the target researcher in the output list.
5. The program must output the results in a valid JSON array of objects format directly to standard output. 
   Example format: `[{"name": "Dr. Bob Jones"}, {"name": "Dr. Carol White"}]`
6. Sort the output JSON array alphabetically by the co-author's name to ensure consistency.
7. Compile your program to `/home/user/coauthor_query` using `g++`.
8. Execute your program with the argument `"Dr. Alan Turing"` and redirect the standard output to `/home/user/coauthors.json`.

Ensure your logic correctly matches paper IDs and avoids the implicit cross join bug the researcher previously encountered.
I am a researcher trying to organize and analyze a dataset of academic publications, but I suspect the database I was given is messy. I have an SQLite database located at `/home/user/research_data.db`.

I was told the database contains tables for authors, papers, and citations, but there is also a "cache" or "index" table in there that is notoriously corrupted and returns stale, mathematically impossible rows. 

I need you to do the following:
1. Reverse engineer the data model of `/home/user/research_data.db` to identify the core, normalized tables (ignore any denormalized cache or summary tables that might contain stale data).
2. Write a Python script to build a citation graph from the true relationships.
3. Calculate the "in-degree" (number of incoming citations) for every paper in the network.
4. Perform a cross-query aggregation to calculate the "Author Impact Score" for each author. An author's impact score is the sum of the in-degrees of all the papers they have authored.
5. Identify the top 3 authors by their impact score (in descending order, resolving ties by alphabetical order of the author's name).
6. Save the results to `/home/user/top_authors.json`.
7. Verify that your final output strictly conforms to the JSON schema located at `/home/user/schema.json`.

Please write and execute the necessary Python scripts and shell commands to complete this task. Make sure the output file strictly follows the schema.
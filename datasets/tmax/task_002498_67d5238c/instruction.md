I am a researcher organizing academic datasets, and I need help migrating my legacy relational citation data (in CSV format) into a Neo4j graph database. 

I previously designed the exact graph schema and cross-representation mapping strategy, but I only have it saved as an image of my whiteboard diagram located at `/app/schema_diagram.png`. The diagram contains the exact Cypher `MERGE` query template you should use.

Please do the following:
1. Inspect the image at `/app/schema_diagram.png` to recover the Cypher query template. It defines how an entity with an integer ID connects to an entity with a string identifier (ISSN).
2. Write a C program at `/home/user/build_queries.c` that performs the parameterized query construction. 
3. The program must read from standard input (`stdin`). Each line of input will be a comma-separated pair: an integer (the researcher ID) and a string (the journal ISSN, up to 20 alphanumeric characters), like so: `1234,1234567X`.
4. For each line read, the C program should print the corresponding Cypher query to standard output (`stdout`), followed by a newline. Do this until the end of the file (EOF) is reached.
5. Compile your C program to the executable `/home/user/build_queries` (e.g., using `gcc -O2 /home/user/build_queries.c -o /home/user/build_queries`).

Ensure your output exactly matches the template from the diagram, replacing the placeholders with the parsed values. Do not print any extra text, prompts, or debugging information to `stdout`.
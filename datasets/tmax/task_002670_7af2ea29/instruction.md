I am a researcher organizing a massive, legacy dataset of academic papers, authors, and citation networks left by a retired colleague. The data is stored in a SQLite database located at `/home/user/research_data.sqlite`. 

Unfortunately, the database schema is entirely obfuscated. The tables are simply named `tbl_A`, `tbl_B`, `tbl_C`, and `tbl_D`, and their columns have generic names. However, based on my knowledge of the domain, the database models four distinct entities/relationships:
1. **Authors**: Contains a unique ID and the author's full name.
2. **Papers**: Contains a unique ID, the paper's title, and the publication year.
3. **Authorships**: A many-to-many linking table connecting Authors to the Papers they wrote.
4. **Citations**: A many-to-many linking table representing citations between papers (which paper cites which other paper).

I need to extract an **Author-to-Author Citation Graph** to feed into my graph analysis software. I need you to reverse engineer the schema, write a C++ program to project this relational data into an aggregated graph edge list, and execute it.

Here are the requirements:
1. Examine the database `/home/user/research_data.sqlite` to identify which table corresponds to Authors, Papers, Authorships, and Citations.
2. Write a C++ program located at `/home/user/extract.cpp` that connects to the SQLite database (using the `sqlite3` C-API).
3. The C++ program must execute a complex SQL query that projects the paper citations into an aggregated author-to-author citation graph. 
   - An edge exists from Author X to Author Y if a paper authored by X cites a paper authored by Y.
   - You must **filter out self-citations** (i.e., Author X citing Author X must be ignored).
   - The edge weight is the total count of such citations between the two authors.
4. The C++ program must output a Tab-Separated Values (TSV) file at `/home/user/author_citations.tsv`.
   - The file should have no header.
   - Each line must be exactly: `Source_Author_Name\tTarget_Author_Name\tCitation_Weight`
   - The output must be sorted by `Citation_Weight` in descending order. If there is a tie, sort by `Source_Author_Name` alphabetically (ascending), and then by `Target_Author_Name` alphabetically (ascending).

To execute the code, ensure your script can be compiled with:
`g++ -std=c++17 /home/user/extract.cpp -lsqlite3 -o /home/user/extract`

Once compiled, run the executable so that `/home/user/author_citations.tsv` is generated.
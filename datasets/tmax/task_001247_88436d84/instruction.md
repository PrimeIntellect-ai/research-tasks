I am a researcher organizing a dataset of academic papers to study collaboration networks. I have my data in two different formats:
1. Document metadata in JSON format: `/home/user/dataset/papers.json`
2. Relational authorship mappings in CSV format: `/home/user/dataset/authors.csv`

I need you to write a C program that processes these files, builds a co-authorship graph, and calculates the degree centrality (number of unique co-authors) for each author. 

Here are the requirements:
1. **Dependency Management**: You may need to install libraries to parse JSON in C (e.g., `libjson-c-dev`). Use standard C and whatever Ubuntu package you need via `sudo apt-get`. (You can use `sudo` for `apt-get` without a password).
2. **Cross-Representation Parsing**: 
   - `papers.json` is an array of objects: `[{"paper_id": 1, "title": "Graph Theory", "year": 2021}, ...]`
   - `authors.csv` has the header `paper_id,author_name` and maps paper IDs to author names.
3. **Graph Analytics**: Build an undirected, unweighted graph where nodes are authors. An edge exists between two authors if they co-authored *at least one* paper. Calculate the degree of each author (the number of unique co-authors they have).
4. **Pipeline Output**: Write a C program `/home/user/workspace/analyze_graph.c`, compile it to `analyze_graph`, and run it. 
5. The program must output the top 3 authors with the highest degree centrality to `/home/user/results/top_authors.txt`.
   - Format each line exactly as: `AuthorName:Degree`
   - If there is a tie in degree, sort the tied authors alphabetically (A-Z) by their `author_name`.
   - Ensure the directory `/home/user/results` exists.

Please create the C code, compile it, and generate the final output file.
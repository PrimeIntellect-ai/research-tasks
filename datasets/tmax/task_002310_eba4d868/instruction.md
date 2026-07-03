You are acting as an assistant for a researcher who is organizing a dataset of scientific papers to analyze citation networks and knowledge domains. 

Your task is to analyze this dataset using MongoDB's NoSQL aggregation pipelines and graph lookup capabilities, driven by a Go program.

Here is what you need to do:

1. **Database Setup**:
   MongoDB is installed on the system. Start a local MongoDB instance as the current user. 
   First, create a directory for the database: `mkdir -p /home/user/data/db`
   Then, start the server in the background: `mongod --dbpath /home/user/data/db --logpath /home/user/mongo.log --bind_ip 127.0.0.1 --port 27017 --fork`

2. **Data Import**:
   The researcher has provided a dataset at `/home/user/papers.json`. Import this file into the local MongoDB instance into a database named `research` and a collection named `papers`. The file contains a JSON array of documents.
   (Hint: You can use `mongoimport --uri="mongodb://127.0.0.1:27017/research" --collection=papers --jsonArray --file=/home/user/papers.json`)

3. **Go Script**:
   Write a Go script at `/home/user/analyze.go`. Ensure you initialize a go module (`go mod init research`) and get the mongo driver (`go get go.mongodb.org/mongo-driver/mongo`).
   The Go script must connect to `mongodb://127.0.0.1:27017` and do the following on the `research.papers` collection:
   
   A. **Index Strategy**: Create an ascending index on the `topics` field to optimize the initial filtering stage of our query.
   
   B. **Graph Aggregation Pipeline**: Execute an aggregation pipeline that performs the following steps in order:
      - **Match**: Filter papers to only those that include `"Machine Learning"` in their `topics` array.
      - **Graph Lookup**: Use `$graphLookup` to trace the citation network. 
        - Start with the `citations` array of the matched papers.
        - Connect from the `citations` field.
        - Connect to the `_id` field.
        - Output the matched network as `citation_network`.
        - Set `maxDepth` to 1 (this finds papers cited directly, and papers cited by those papers).
      - **Add Fields**: Create a new field `network_size` which is the size (`$size`) of the `citation_network` array. This serves as a proxy for the paper's graph centrality/influence in this local subgraph.
      - **Sort**: Sort the results by `network_size` descending. If there is a tie, sort by `_id` ascending.
      - **Limit**: Keep only the top 3 papers.
      - **Project**: Output only the `_id` and `network_size` fields (exclude other fields like the original citations or the large graph array).

4. **Output**:
   The Go script must write the final result of the aggregation as a formatted JSON array to `/home/user/top_papers.json`.
   The format should look exactly like this:
   ```json
   [
     {
       "_id": "paper_1",
       "network_size": 4
     },
     ...
   ]
   ```

Run your Go script to produce the output file.
You are an AI assistant helping a data researcher organize their dataset lineage. 

The researcher has two files in `/home/user/`:
1. `datasets.csv`: Contains dataset IDs and names.
2. `relationships.csv`: Contains source dataset IDs, target dataset IDs, and the transformation applied.

The researcher wrote a Bash script, `/home/user/extract_edges.sh`, to join these files and export an edge list of the dataset knowledge graph. However, the script is broken. Due to an implicit cross-join in the nested loops, it outputs every possible combination of datasets for every transformation, rather than matching the specific IDs.

Your tasks are:
1. **Fix the script:** Modify `/home/user/extract_edges.sh` so that it correctly joins the files. It must output exactly one line per valid relationship in the format:
   `Source_Dataset_Name|Target_Dataset_Name|Transformation_Type`
   Run your fixed script and save the output to `/home/user/edges.txt`. Do not include the CSV headers in the output.

2. **Graph Traversal:** Using the corrected data, find the shortest lineage path (fewest number of transformations) from `Raw_Climate_Data` to `Global_Warming_Model`. 
   
3. **Format Conversion & Output:** Write the sequence of dataset names in this shortest path to `/home/user/path.txt`. The file should contain one dataset name per line, starting with `Raw_Climate_Data` and ending with `Global_Warming_Model`.

Ensure both `/home/user/edges.txt` and `/home/user/path.txt` exist and contain the correct results.
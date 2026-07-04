You are an AI assistant helping a data researcher organize their complex dataset pipelines. 

The researcher has hundreds of datasets that depend on each other, transformed by various scripts. They have an unordered raw log file of these dataset dependencies located at `/home/user/dataset_edges.csv`. The CSV has three columns: `SourceDataset`, `TargetDataset`, and `ProcessingTimeHours`.

Your task is to write a Go program (or multiple) to process this lineage graph, build an efficient index, and find the shortest processing path to produce a specific target dataset.

Here are your specific requirements:

1. **Index Generation**: Write a Go program that reads `/home/user/dataset_edges.csv` and builds an adjacency list index, saving it to `/home/user/graph_index.json`. The JSON should be an object where keys are source datasets, and values are arrays of objects containing `target` (string) and `cost` (integer).
   Example format:
   ```json
   {
     "Raw_Data": [{"target": "Clean_Data", "cost": 2}]
   }
   ```

2. **Graph Traversal**: Read `/home/user/graph_index.json` and compute the shortest path (in terms of `ProcessingTimeHours`) from `Raw_Alpha` to `Final_Omega`. 

3. **Output Schema**: Save the final shortest path result to `/home/user/path_result.json`. The output must strictly adhere to the following structure exactly (output schema validation will be performed on it):
   ```json
   {
     "source": "<starting dataset name>",
     "target": "<ending dataset name>",
     "total_time_hours": <integer total cost>,
     "path": [
       "<dataset 1>",
       "<dataset 2>",
       "..."
     ]
   }
   ```
   
Please put all your Go code in `/home/user/` and compile/run it to generate the final `path_result.json`. The final JSON must be pretty-printed or minified, but its key structure and types must be perfectly correct.
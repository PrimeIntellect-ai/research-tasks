A researcher is organizing a dataset from a recent experiment recorded in a video file located at `/app/experiment_record.mp4`. We need to extract visual metrics from this video, map them into a knowledge graph to track the temporal relationships, and perform analytical aggregation to find segments with high variance in illumination.

Your task consists of the following steps:

1. **Video Processing**: 
   Read the video `/app/experiment_record.mp4`. For every frame, convert it to grayscale and calculate its mean pixel intensity (a float between 0 and 255). Keep track of the frame index (starting at 0).

2. **Knowledge Graph Construction**:
   Use Python's `rdflib` to construct an in-memory RDF knowledge graph representing the video frames. 
   - Define a namespace `http://example.org/video#`.
   - Represent each frame as a resource (e.g., `ex:Frame_0`, `ex:Frame_1`).
   - Add triples indicating the frame index: `ex:Frame_0 ex:hasIndex 0` (integer).
   - Add triples for the mean intensity: `ex:Frame_0 ex:hasIntensity 120.5` (float).
   - Add sequence edges linking each frame to the next: `ex:Frame_0 ex:hasNext ex:Frame_1`.

3. **Graph Querying**:
   Write and execute a SPARQL query against your graph to retrieve the `frame_index` and `intensity` for all frames. Extract this data into a structured format (like a list of dictionaries).

4. **Window Functions & Aggregation**:
   Load the SPARQL query results into a Pandas DataFrame. 
   - Sort the data strictly by `frame_index` in ascending order.
   - Use Pandas window functions to calculate the rolling sample variance of the `intensity` over a window of 5 frames (i.e., the current frame and the 4 preceding frames). 
   - Drop the rows where the rolling variance is NaN (the first 4 frames).
   
5. **Output**:
   Save the final filtered DataFrame to `/home/user/results.csv`.
   The CSV must contain exactly two columns: `frame_index` (integer) and `rolling_variance` (float), sorted by `frame_index` ascending.

Make sure to install any necessary Python packages (like `opencv-python-headless`, `rdflib`, `pandas`) before running your script.
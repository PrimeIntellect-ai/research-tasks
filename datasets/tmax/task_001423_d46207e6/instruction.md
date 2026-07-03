You are a data engineer building a lightweight ETL pipeline. Your task is to extract location data from two different sources, normalize the data, orchestrate the pipeline using a DAG tool (`make`), and compute spatial similarity to find matching locations.

All work should be done in the `/home/user/etl_pipeline` directory.

I have placed two raw data files in this directory:
1. `source_A.csv`: Contains locations in standard CSV format (`id,lat,lon`).
2. `source_B.json`: Contains locations in a nested JSON array format.

You need to build a multi-language pipeline that does the following:

**1. Normalization Step:**
Write a bash script or use `jq` to process `source_B.json` and output a normalized CSV file named `source_B_norm.csv` with exactly the same header format as source A: `id,lat,lon`. The ID field from the JSON is called `loc_id`, and the coordinates are nested under `coordinates.latitude` and `coordinates.longitude`.

**2. Distance Computation Step:**
Write a Python 3 script named `match.py` that reads both `source_A.csv` and `source_B_norm.csv`. 
It must compute the Haversine distance (in kilometers) between every point in Source A and every point in Source B. 
Use Earth's radius `R = 6371.0` km.
The script should output a file named `matches.csv` containing only the pairs of locations that are within a distance of **5.0 km** (inclusive).
The output `matches.csv` must have the header `id_A,id_B,distance_km`. 
The `distance_km` should be rounded to exactly 2 decimal places (e.g., `2.55`).
Sort the output rows ascendingly by `id_A`, then by `id_B`.

**3. Pipeline DAG Orchestration:**
Create a `Makefile` in the same directory to orchestrate this DAG. It must have the following targets:
- `normalize`: Generates `source_B_norm.csv` from `source_B.json`.
- `match`: Generates `matches.csv`. It must explicitly declare `source_A.csv`, `source_B_norm.csv`, and `match.py` as dependencies.
- `all`: The default target, which should depend on `match`.

Ensure that running `make all` from a clean state successfully executes the entire pipeline and generates `matches.csv`. Do not run `make` yourself; just write the files.
You are a data scientist analyzing environmental DNA (eDNA) data mapped over a 2D spatial grid. Your goal is to construct a pipeline that filters out contaminated sequence data and fits the clean data to a spatial mesh model using a local multi-service architecture.

There are three tasks you must complete:

1. **Service Configuration and Composition**
We have three services that must work together, but their configuration is broken. The services are started via `/app/start_services.sh`. 
- **Mesh API:** A Flask application serving spatial mesh data in HDF5 format on port 8080.
- **Cache:** A Redis instance running on port 6379.
- **Stats Ingestion Worker:** A Python worker that processes spatial datasets, fetches reference data from the Mesh API, and caches the fitted statistical parameters in Redis.
Create a configuration file at `/home/user/services.env` with the appropriate environment variables (`REDIS_HOST`, `REDIS_PORT`, `MESH_API_URL`) so that when `/app/start_services.sh` is executed, the stats worker can successfully perform an end-to-end run.

2. **Adversarial Sequence Filter**
Contamination in the sequencing run has introduced artifactual reads. You must write a Python script at `/home/user/filter_sequences.py` that acts as a classifier to filter out "evil" FASTA files from "clean" ones.
- **Invocation:** `python3 /home/user/filter_sequences.py <path_to_fasta>`
- **Logic:** The script must read the FASTA file. If 5% or more of the sequences in the file contain the specific primer sequence `GATCGGAAGAGCACACGTCTG` (allowing for at most 1 nucleotide mismatch), the file is classified as contaminated (evil).
- **Output:** The script must exit with status code `1` if the file is contaminated (evil), and exit with status code `0` if the file is clean. 

3. **Validation**
Run your script against the unlabelled datasets in `/app/data/samples/` to ensure it works, but be prepared: your script will be tested against hidden clean and evil corpora.

Ensure your `services.env` file is perfectly configured to allow the stats worker to report a "PIPELINE_SUCCESS" in `/home/user/worker.log`.
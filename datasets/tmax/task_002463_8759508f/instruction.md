You are tasked with fixing and completing an artifact curation workflow for a binary repository.

System Context:
Our system receives telemetry artifacts in chunked, text-encoded formats. We need a curation script to assemble these chunks, process their metadata, tightly compress the binary data, and expose the results via Nginx and Redis.

The incoming files are stored in `/home/user/incoming/`. Each artifact (e.g., `alpha`, `beta`) has:
1. Multiple data chunks named `<artifact>.partNN` (e.g., `alpha.part01`, `alpha.part02`). These contain a continuous hexadecimal dump of the raw telemetry binary.
2. A metadata file named `<artifact>.meta`, encoded in UTF-16LE.
3. A trigger file named `<artifact>.done` indicating the upload is complete.

Your objective is to write a bash script at `/home/user/curate.sh` that processes all artifacts currently in `/home/user/incoming/` that have a `.done` marker. For each complete artifact, the script must:

1. **Merge and Convert**: Assemble the `.partNN` files in numerical order. The combined data is a pure hex string. You must convert this hex string back into the original raw binary data.
2. **Compress**: Compress the raw binary data. You are evaluated on the storage efficiency of your artifacts. To pass, the total size of all compressed artifacts combined must be less than 850,000 bytes. Move the highly-compressed binary to `/home/user/artifacts/<artifact>.bin.xz` (or `.gz`, `.bz2`, as long as it's highly compressed).
3. **Metadata Encoding & Redis**: Convert the `<artifact>.meta` file from UTF-16LE to UTF-8. Extract the string value next to `Author: ` (e.g., if the line is `Author: Alice`, extract `Alice`). Insert this value into a local Redis instance under the key `meta:author:<artifact>`.
4. **Service Integration**: 
   - Ensure a local Redis server is running on port `6379` (you may start it in the background).
   - Ensure Nginx is running on port `8080`, configured to serve static files from `/home/user/artifacts/`. A configuration file is already prepared at `/home/user/nginx.conf`. Start Nginx using this specific config (e.g., `nginx -c /home/user/nginx.conf`).

Requirements:
- Create `/home/user/artifacts/` if it does not exist.
- Your script `/home/user/curate.sh` must complete the entire workflow when executed.
- Ensure all services (Redis, Nginx) are running and properly populated/serving before you finish.
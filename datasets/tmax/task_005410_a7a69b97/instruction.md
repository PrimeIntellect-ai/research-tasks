You are a Database Reliability Engineer managing a graph-based backup metadata catalog. Recently, a legacy reporting script crashed our NoSQL database because an implicit cross-join in its backup lineage query caused a combinatorial explosion and subsequent OOM error. 

We need you to implement a fast, recursive Python-based API service that safely resolves backup lineages without bringing down the database.

A colleague left a voicemail regarding the incident, which has been saved to `/app/incident_call.wav`. This audio contains the secret authentication token you must use to secure the new API.

Here are your instructions:
1. **Transcribe the audio:** Listen to/transcribe `/app/incident_call.wav` to discover the required API auth token.
2. **Analyze the Data:** Read the backup metadata graph located at `/app/backups.json`. It contains an array of JSON objects representing backup nodes. Each node has an `id`, a `parent_id` (which is `null` for root backups), and a `timestamp` (ISO 8601 format).
3. **Build the Service:** Create a Python HTTP server (you may use Flask, FastAPI, or standard library `http.server`) listening precisely on `127.0.0.1:9090`.
4. **Implement the Lineage Endpoint:** 
   - Expose the endpoint `GET /lineage?id=<backup_id>`.
   - The endpoint must recursively traverse the parent-child backup graph to find all ancestors of the requested `backup_id` up to the root.
   - The returned array must *include* the requested ID itself and be strictly sorted by `timestamp` in ascending order.
   - Output schema must strictly follow this JSON structure: `{"lineage": ["B-100", "B-101", ...]}`.
   - Return HTTP 404 if the requested `id` does not exist in the dataset.
5. **Secure the Endpoint:** The endpoint must require the header `Authorization: Bearer <TOKEN>`, where `<TOKEN>` is the exact phrase spoken in the audio file. Return HTTP 401 for missing or incorrect tokens.

Ensure your service stays running in the foreground or background so that our automated systems can query it.
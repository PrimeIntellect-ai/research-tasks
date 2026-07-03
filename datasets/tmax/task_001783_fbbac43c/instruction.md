You are acting as an automated release manager. You have been given several microservice deployment manifests, and you need to consolidate their dependencies and expose a deployment API.

In the directory `/home/user/manifests`, there are several JSON files representing different microservices. Each file contains a "deps" dictionary mapping package names to version strings.

Your task is to:
1. Parse all JSON files in `/home/user/manifests`.
2. Merge all dependencies into a single consolidated dictionary. 
3. Resolve version conflicts: if multiple services depend on the same package, you must select the highest version. Use standard lexicographical string comparison for the version strings (e.g., "2.26.0" > "2.25.1").
4. Sort the final consolidated dependencies alphabetically by package name.
5. Create a Python script at `/home/user/api.py` that starts a REST API server on port `8123` (binding to `0.0.0.0` or `localhost`). You may use standard libraries (like `http.server`) or install a framework like `Flask` or `FastAPI`.
6. The API must have a `GET /manifest` endpoint. When requested, it must return a JSON response with a single key `"dependencies"` containing the merged and sorted dictionary. 
7. Run your API server in the background so it is actively listening on port 8123 when you complete the task.

Example expected response from `GET /manifest`:
```json
{
  "dependencies": {
    "flask": "1.1.2",
    "requests": "2.26.0"
  }
}
```

Ensure the server is running and accessible via `curl http://localhost:8123/manifest` before you finish.
I've been migrating an old Python 2 API backend to Python 3, but I'm running into errors and I need your help to fix them and test the system.

The project is located in `/home/user/api_project`. It consists of a custom REST API built with `http.server` and an Nginx reverse proxy. 

Here is what you need to do:

1. **Fix the Python 3 Migration Bugs**:
   The backend server is in `/home/user/api_project/server.py`. It is supposed to run on port 8080. It has a POST endpoint at `/api/merge_sort` that takes a JSON payload containing two lists of objects, merges them, and sorts them by the `id` key. 
   However, the migration wasn't completely successful. The code still uses some Python 2 idioms (specifically for sorting and dictionary iteration) that cause crashes in Python 3. Find and fix these Python 2 remnants so the script works perfectly in Python 3.

2. **Fix the Reverse Proxy**:
   There is a local Nginx configuration file at `/home/user/api_project/nginx.conf`. It is supposed to listen on port 8000 and proxy all requests starting with `/api/` to the backend server. There is a configuration error preventing it from routing traffic to the correct backend port. Fix the typo in the configuration file.

3. **Start the Services**:
   Start the Python backend server in the background. Then, start Nginx in the background using the provided configuration file (e.g., `nginx -c /home/user/api_project/nginx.conf -g 'daemon off;' &`).

4. **Test the Endpoint**:
   Write a Python test script at `/home/user/api_project/test.py` that sends a POST request to the *reverse proxy* (`http://127.0.0.1:8000/api/merge_sort`) with the following JSON payload:
   ```json
   {
     "list1": [{"id": 5, "name": "Echo"}, {"id": 1, "name": "Alpha"}, {"id": 3, "name": "Charlie"}],
     "list2": [{"id": 4, "name": "Delta"}, {"id": 2, "name": "Bravo"}]
   }
   ```
   The script should parse the JSON response and write it exactly as a formatted JSON array (with no extra wrapper keys, just the merged and sorted list of objects) to `/home/user/api_project/result.json`.

Ensure your fixes leave the system running and the final sorted result correctly written to the file.
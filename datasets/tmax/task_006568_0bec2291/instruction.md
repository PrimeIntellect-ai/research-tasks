You are an observability engineer tasked with tuning the backend services for a set of monitoring dashboards. Some of the dashboard data source containers have a known memory leak that causes "Dashboard UI Error" logs to be emitted, eventually leading to a crash. 

You have been provided with a container management script at `/home/user/container_mgr.sh` that simulates a container runtime. 

Your task is to write a Go program `/home/user/auto_tuner.go` that performs the following automated remediation and reporting:

1. **Identify High-Memory Containers:** 
   Your Go program must execute `/home/user/container_mgr.sh list` and use text processing tools (like `awk`, which you should invoke via Go's `os/exec`) to identify containers whose memory usage exceeds `500MB`.
   
   *Example `list` output:*
   ```text
   CONTAINER ID   IMAGE      STATUS   MEM USAGE
   abc12345       dash-app   Running  250MB
   def67890       dash-app   Running  600MB
   ```

2. **Restart Containers:**
   For any container exceeding 500MB, your Go program must restart it by executing `/home/user/container_mgr.sh restart <CONTAINER ID>`.

3. **Extract Errors:**
   For **all** containers initially listed, your Go program must extract the specific UI error messages from their logs. You must fetch the logs by executing `/home/user/container_mgr.sh logs <CONTAINER ID>` and piping the output through `grep "Dashboard UI Error"` (using Go's `os/exec`). Extract only the error description (the text after "Dashboard UI Error: ").

4. **Generate Report:**
   The Go program must compile its findings into a strictly formatted JSON file at `/home/user/observability_report.json`. 

   The format must exactly match this structure:
   ```json
   {
     "restarted_containers": ["<id1>", "<id2>"],
     "ui_errors": {
       "<id1>": [
         "Widget 'CPU' timeout.",
         "Data source unavailable."
       ],
       "<id3>": [
         "Widget 'Memory' render failure."
       ]
     }
   }
   ```
   *Note: Only include containers in `ui_errors` if they actually had "Dashboard UI Error" logs. Ensure the JSON is properly formatted.*

Build and execute your Go program to perform the remediation and generate the final report file.
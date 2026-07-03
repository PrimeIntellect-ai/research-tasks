You are an observability engineer tuning some local dashboards. We need a mechanism to log a specific metric every time a dashboard configuration is updated and committed to our local Git repository.

Please perform the following steps:

1. Write a C program at `/home/user/metric_logger.c` and compile it to `/home/user/metric_logger`.
   The program must do the following interactively (via stdin/stdout):
   - Print "Enter metric name: " (no newline).
   - Read a string (up to 99 characters).
   - Print "Enter metric value: " (no newline).
   - Read an integer.
   - Append a JSON formatted string `{"metric": "<name>", "value": <value>}` followed by a newline to `/home/user/dashboard_metrics.log`.
   - Exit cleanly.

2. Initialize a local Git repository in the directory `/home/user/dash_config`.

3. We need to automate interacting with the `metric_logger` binary. Write an `expect` script at `/home/user/push_metric.exp` that runs `/home/user/metric_logger` and automatically answers the prompts:
   - For the metric name, send `dashboard_updates`
   - For the metric value, send `1`
   Make sure the `expect` script is executable.

4. Create a Git hook in `/home/user/dash_config/.git/hooks/post-commit` that simply executes `/home/user/push_metric.exp`. Ensure the hook is executable.

5. Finally, test the end-to-end flow:
   - Create a file named `dash.json` in `/home/user/dash_config` containing exactly `{"refresh": 5}`.
   - Stage the file and commit it with the message "Initial dashboard config" to trigger the `post-commit` hook.

By the end of this task, the commit should have been made, the hook should have triggered the expect script, which in turn fed the inputs to the C program, writing the final JSON log to `/home/user/dashboard_metrics.log`.
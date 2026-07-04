You are tasked with restoring an alert aggregation endpoint for a legacy monitoring system. 

We have an undocumented, stripped binary located at `/app/prober`. This binary acts as a legacy node that sends health metrics and alerts, but the original receiver service has been lost. 

Your objectives are:

1. **Reverse Engineer the Protocol:**
   Analyze the `/app/prober` binary to determine the exact TCP protocol it uses to communicate. It sends specific initialization strings, metric payloads, and teardown sequences.

2. **Develop the Alert Receiver (C):**
   Write a C program at `/home/user/alert_receiver.c` and compile it to `/home/user/alert_receiver`. 
   - This service must listen on `127.0.0.1:9090`.
   - It must perfectly implement the server-side of the protocol expected by the prober.
   - For every alert received (which contains a metric name and value), the receiver must append a line to `/home/user/alerts.log` in the exact format: `[ALERT_RECEIVED] metric_name: value` and then send the appropriate acknowledgment back to the client.
   - The service must handle multiple sequential connections and remain running in the background.

3. **Port Forwarding Setup:**
   The legacy prober is hardcoded to connect to `127.0.0.1:8080`. You must use SSH local port forwarding to forward connections from `127.0.0.1:8080` to your receiver on `127.0.0.1:9090`. 
   - We have provided a local user account `monitor_user` with the password `monitor_pass`. 
   - Write an `expect` script at `/home/user/start_tunnel.exp` that automates logging into SSH as `monitor_user@127.0.0.1` with the given password to establish the port forward in the background.

Ensure your compiled C program is running and your `expect` script has established the tunnel. The automated verification will interact with your service via both port 9090 and 8080 using the protocol expected by the prober.
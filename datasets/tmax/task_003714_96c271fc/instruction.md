Wake up, you're on-call and we have a Sev-1 outage. It's 3:00 AM. 

Our Go-based API CacheService has completely crashed after a botched deployment, and the configuration file was accidentally deleted from the server. The only record of the production configuration we have is a screenshot of the monitoring dashboard taken right before the crash, located at `/app/dashboard_error.png`. 

Furthermore, the latest deployment introduced a regression that causes the service to panic when the `/health` endpoint is hit. 

Your objectives:
1. Extract the missing `PORT` and `AUTH_TOKEN` from the text within the `/app/dashboard_error.png` image.
2. Navigate to the Git repository at `/home/user/cache-service`.
3. Use Git bisection or log inspection to find the recent commit that introduced a panic in the `/health` handler.
4. Fix the Go code to remove the panic.
5. Build and start the Go service using the recovered `PORT` and `AUTH_TOKEN`. Run it in the background so it is actively listening.

The service must be started as:
`PORT=<recovered_port> AUTH_TOKEN=<recovered_token> ./cache-service &`

The automated verification system will send real HTTP protocol requests to the `/health` endpoint using the credentials and port you extracted. Leave the fixed service running.
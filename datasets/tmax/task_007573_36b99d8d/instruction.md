You are an observability engineer tuning local dashboards. You have a custom metrics service written in C that acts as a backend, and you need to set up a reverse proxy to access it alongside a future UI. Currently, the local development setup is broken. 

There are three tasks you need to complete:

**1. Fix the C Metrics Service**
The source code for the metrics service is located at `/home/user/metrics_service.c` (assume it exists, but you can overwrite it with the fixed version). The service is supposed to listen on a port provided via command-line arguments and serve a simple HTTP JSON response. However, it fails to bind to the correct port due to a network byte-order bug in the socket configuration.
Identify the bug (hint: look at how `sin_port` is assigned), fix the C code, and compile it to `/home/user/metrics_service` using `gcc`.

Here is the current broken code of `/home/user/metrics_service.c`:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    int port = atoi(argv[1]);
    int server_fd;
    struct sockaddr_in address;
    int opt = 1;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) return 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    // BUG: Missing network byte order conversion
    address.sin_port = port;

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) return 1;
    if (listen(server_fd, 3) < 0) return 1;

    char response[] = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{\"status\": \"ok\", \"active_connections\": 42}\n";
    while(1) {
        int new_socket = accept(server_fd, NULL, NULL);
        if (new_socket >= 0) {
            write(new_socket, response, strlen(response));
            close(new_socket);
        }
    }
    return 0;
}
```

**2. Configure the Reverse Proxy**
Create an Nginx configuration file at `/home/user/nginx.conf`. 
Since you are running as an unprivileged user, your Nginx config must be self-contained in `/home/user`. It must:
- Run with `worker_processes 1;`
- Store its pid at `/home/user/nginx.pid`
- Store access log at `/home/user/access.log` and error log at `/home/user/error.log`
- Define the `client_body_temp_path`, `proxy_temp_path`, `fastcgi_temp_path`, `uwsgi_temp_path`, and `scgi_temp_path` directives all pointing to `/home/user/tmp/` (you will need to create this directory).
- Listen on port `8080`.
- Proxy all requests for the path `/api/metrics` to the C metrics service running at `http://127.0.0.1:9090`.

**3. Write an Idempotent Deployment Script**
Write a bash script at `/home/user/deploy.sh` (ensure it is executable) that safely and idempotently starts the environment:
- Create `/home/user/tmp/` if it does not exist.
- Gracefully kill any existing Nginx processes using `/home/user/nginx.pid` and any running instances of `/home/user/metrics_service`.
- Start the compiled C service in the background, listening on port `9090`: `/home/user/metrics_service 9090 &`
- Start Nginx in the background using your custom config: `nginx -c /home/user/nginx.conf &`

Run your `./deploy.sh` script to verify everything works. The automated test will check if a `GET` request to `http://127.0.0.1:8080/api/metrics` successfully returns the JSON payload.
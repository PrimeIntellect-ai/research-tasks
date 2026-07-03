You are a monitoring specialist tasked with setting up a custom alert and health-check service for our legacy network systems. 

We received a configuration snippet as a screenshot from an old virtualization setup, which is saved at `/app/network_diagram.png`. 
Your tasks are as follows:

1. Extract the text from `/app/network_diagram.png`. You may use `tesseract` (which is preinstalled) or any script to read the image. The image contains three key pieces of information:
   - `PORT: <number>`
   - `ENDPOINT: <path>`
   - `AUTH_KEY: <string>`

2. Write a custom C program at `/home/user/monitor.c` that acts as a standalone HTTP/1.0 server.
3. The C program must listen on the `PORT` extracted from the image.
4. It must respond to `GET` requests on the extracted `ENDPOINT`. 
5. When a valid request is made to the endpoint, the server must respond with a `200 OK` status and a plain text body containing exactly the `AUTH_KEY` extracted from the image, followed by a newline.
6. For any other path, it should return a `404 Not Found`.
7. Compile your C program to `/home/user/monitor_service` and run it in the background so it is actively listening.
8. Write an idempotent bash script at `/home/user/manage_service.sh` that checks if the service is running, and starts it if it is not.

Leave the service running when you are finished. Automated tests will send HTTP GET requests to your service to verify it is working correctly.
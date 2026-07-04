I am a researcher organizing large datasets. I have a custom, lightweight C-based HTTP server that streams a dataset directory on-the-fly as an uncompressed tar archive. This tool avoids creating intermediate tarballs on disk by memory-mapping the files and streaming them directly over HTTP.

The source code for this tool is vendored at `/app/micro-tar-server-1.0`.

However, the tool has a couple of issues preventing me from using it in our non-root environment:
1. It fails to start because it tries to bind to a privileged port by default. 
2. When archiving directories that contain symbolic links, the archiving logic crashes because it attempts to memory-map (`mmap`) the symbolic links themselves instead of adding them as symlink entries in the tar header.

I need you to:
1. Fix the source code in `/app/micro-tar-server-1.0` so that:
   - It listens on port `8080` instead of its default port.
   - It correctly handles symbolic links by adding them to the streamed tar archive as symlink entries (without trying to `mmap` their contents). 
2. Compile the fixed application.
3. Start the server in the background so it listens on `127.0.0.1:8080`. 

The server requires an API token to allow downloads. Make sure the server runs and accepts requests with the header: `Authorization: Bearer ds-secret-token`.

My dataset is located at `/home/user/dataset_active`. The server takes the directory to serve as a command-line argument. Once the server is running, do not terminate it; it must remain running in the background for my automated verification scripts to download the archive.

Please make the necessary code modifications, compile the tool, and run it.
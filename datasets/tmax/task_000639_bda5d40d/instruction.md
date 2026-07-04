You are building the backend for a custom Binary Artifact Manager. 

The system relies on a repository of binary artifact files located in `/home/user/artifacts/`. Each file is named `<id>.bin`. 
However, the dependencies between these artifacts are messy and contain circular references (infinite loops). Your job is to build an API service that parses these binary files, securely resolves dependencies without getting stuck in loops, and serves the data.

### 1. Video Fixture (Authentication & Root Discovery)
There is a video file located at `/app/deploy_sequence.mp4`. 
The first 16 frames of this video contain a sequence of purely black and white frames.
- A black frame represents the bit `0`.
- A white frame represents the bit `1`.
Decode these first 16 frames as a 16-bit unsigned integer (Big-Endian). 
This integer is the `ROOT_ID`. You will need this to authenticate requests.

### 2. Binary Format Parsing
Each `.bin` file in `/home/user/artifacts/` uses a proprietary binary format. All integers are Little-Endian.
- **Bytes 0-3**: Magic bytes `ARTF`
- **Bytes 4-7**: `uint32` Artifact ID
- **Bytes 8-11**: `uint32` Number of dependencies ($N$)
- **Bytes 12 to 12+(4*N)-1**: An array of $N$ `uint32` integers, representing the IDs of dependent artifacts.
- **Bytes 12+(4*N) to 15+(4*N)**: `uint32` Manifest Length ($M$)
- **Bytes 16+(4*N) to end**: $M$ bytes of an XML manifest (e.g., `<artifact><name>lib-core</name><version>1.2</version></artifact>`).

### 3. Service Requirements
Write and run a Python HTTP service (using `Flask`, `FastAPI`, or `http.server`) that listens on `127.0.0.1:8080`.
The verifier will test your service while it is running.

**Authentication:** 
All endpoints MUST require an `Authorization: Bearer <ROOT_ID>` header. If missing or incorrect, return a 401 status code.

**Endpoints:**
1. `GET /manifest/<artifact_id>`
   - Parses the requested artifact's binary file.
   - Extracts the XML manifest.
   - Returns a JSON representation of the XML. For example, if the XML is `<artifact><name>foo</name><version>1</version></artifact>`, return `{"name": "foo", "version": "1"}`. Return 404 if the artifact does not exist.

2. `GET /dependencies/<artifact_id>`
   - Parses the requested artifact and recursively follows all its dependencies.
   - MUST handle circular dependencies (e.g., 101 depends on 102, which depends on 101) without infinite looping.
   - Returns a JSON array of all unique artifact IDs in the dependency tree (excluding the requested artifact itself), sorted in ascending numerical order. Example: `[102, 105, 109]`.

Write your solution in Python, start the server, and leave it running in the background or foreground so the automated verifier can test it.
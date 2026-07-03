You are an artifact manager curating a binary repository. We have received an incoming submission containing a metadata archive and an associated audio artifact. You must parse the metadata, analyze the audio, and serve the combined information via a local API for our ingestion systems.

Here are your instructions:
1. You have a nested metadata archive located at `/app/repo_archive.tar.gz`. This is a gzip-compressed tarball containing a zip file named `internal_data.zip`. 
2. Extract the zip file. Inside, you will find a file named `metadata.xml`. This file is encoded in a legacy format (UTF-16LE).
3. Parse `metadata.xml` to locate the artifact element with `id="audio_1"`. Extract the text contents of its `<author>` tag.
4. You also have an audio artifact located at `/app/artifact.wav`. Process this audio file to transcribe the spoken content. 
5. Identify the very first spoken word in the audio. Convert it to lowercase and strip all punctuation. This is your `transcription_keyword`.
6. Implement and start an HTTP server listening on `127.0.0.1:8080` (you may use any programming language you prefer, such as Python, Node.js, etc.).
7. The server must accept requests and specifically respond to `GET /api/artifact`.
8. The response to `GET /api/artifact` must have a `200 OK` status code and a JSON body containing exactly these two keys:
   - `"author"`: The author name parsed from the XML.
   - `"transcription_keyword"`: The first transcribed word, as processed in step 5.

Keep the HTTP server running in the background so that our automated systems can query it to verify your success.
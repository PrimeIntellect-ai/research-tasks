We are migrating our legacy backend infrastructure from Python 2 to Python 3. A critical piece of our web security and API routing layer is a custom URL parser and constraint checker. Unfortunately, the original Python 2 source code for this router was lost. 

We have a compiled legacy binary (created with pyinstaller from the original Python 2 script) located at `/app/legacy_router_oracle`. It takes a single URL path/query string as a command line argument and outputs a JSON object containing the routed path, parsed parameters, and an authorization status.

Additionally, the original developer left a voice note regarding a specific security constraint and routing quirk that was implemented. You can find this recording at `/app/dev_notes.wav`.

Your task is to write a Python 3 script at `/home/user/new_router.py` that behaves **exactly** like the legacy oracle for all possible URL inputs. 

Requirements:
1. Your script must be executable via: `python3 /home/user/new_router.py "<url_string>"`
2. It must parse the URL and output the exact same JSON format (to stdout) as `/app/legacy_router_oracle` would for the same input.
3. You must listen to/transcribe `/app/dev_notes.wav` to uncover the hidden security routing constraints, as black-box testing alone might miss the specific edge cases mentioned.
4. It must correctly handle all REST and GraphQL routing endpoints and their associated parameter constraints.
5. Exit cleanly with code 0 after printing the JSON.

Please explore the behavior of `/app/legacy_router_oracle` by passing it various URLs (e.g., `/api/users?id=5`, `/graphql?query=test`, `/secure/data?token=...`) to deduce its baseline parameter parsing logic, and combine that with the constraints heard in the audio file.
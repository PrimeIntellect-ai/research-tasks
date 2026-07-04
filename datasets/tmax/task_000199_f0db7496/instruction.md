I'm reviewing a PR for our numerical data processing pipeline, but the contributor completely misunderstood the requirements for the "Quadratic Base64 Serializer" component. I recorded a quick voice memo explaining the correct numerical algorithm and serialization format while I was out walking. 

The audio file is located at `/app/spec_memo.wav`.

Please write a Python script at `/home/user/serializer.py` that reads a JSON array of integers from standard input, applies the exact numerical transformation and serialization format described in the audio, and prints the resulting JSON to standard output. 

Your script must be robust and perfectly match the specification, as it will be rigorously tested against a reference implementation using a fuzzing test suite that checks bit-exact equivalence over thousands of random inputs. You can use any standard Python libraries. Please ensure your script is executable and processes the input correctly.
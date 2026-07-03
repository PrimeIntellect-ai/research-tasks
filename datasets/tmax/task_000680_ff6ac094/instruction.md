You are an AI assistant acting as a Machine Learning Engineer preparing a pipeline for a voice-based customer support system.

Your goal is to build and deploy a local HTTP service that processes audio requests, transcribes them, and classifies the transcription into one of several predefined support intents using text embeddings.

You are provided with:
1. `/app/support_call.wav` - A sample customer support audio clip you can use to test your pipeline.
2. `/app/intents.json` - A JSON file containing a list of support intents and their textual descriptions. The format is a list of objects: `[{"intent_name": "...", "description": "..."}]`.

Your tasks:
1. Create a machine learning pipeline that can transcribe audio to text. You MUST use the `openai/whisper-tiny` model from the HuggingFace `transformers` library for transcription to ensure reproducibility and performance.
2. Create an embedding-based classifier. Compute the text embeddings for all the intent descriptions using the `sentence-transformers/all-MiniLM-L6-v2` model.
3. When a new audio clip is received, transcribe it, compute the embedding of the transcription using the same sentence-transformer model, and find the closest intent based on cosine similarity.
4. Expose this pipeline as a web service. You must start an HTTP server listening on `127.0.0.1:5000`.
5. The server must expose a `POST /predict_intent` endpoint. 
   - The endpoint will receive raw WAV audio data directly in the request body (Content-Type: audio/wav).
   - It must return a JSON response strictly matching this schema: `{"transcription": "<the_transcribed_text>", "intent": "<matched_intent_name>"}`.

You may use any programming language or framework you prefer (e.g., Python with Flask or FastAPI). Make sure your service is running in the background and listening on the specified port before you finish the task. 

Ensure you enforce the exact JSON response schema. The verification system will send multiple WAV files to your endpoint to verify the correctness of the transcription and intent matching.
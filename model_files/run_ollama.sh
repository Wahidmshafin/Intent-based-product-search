#!/bin/bash

echo "Starting Ollama server..."
ollama serve &
# Wait for Ollama HTTP API to respond
echo "Waiting for Ollama server to be active..."
sleep 1

# # Pull the model if it isn’t already present
# if ! ollama list | grep -q 'qwen2.5:3b-instruct'; then
#   echo "Pulling qwen2.5:3b-instruct..."
#   ollama pull qwen2.5:3b-instruct
# fi

if ! ollama list | grep -q 'nomic-embed-text'; then
  echo "Pulling nomic-embed-text..."
  ollama pull nomic-embed-text
fi

# # Finally, run the model in the foreground to keep the container alive
# echo "Running qwen2.5:3b-instruct..."
# ollama run qwen2.5:3b-instruct 

ollama create ecommerce-ner-model -f model_files/Modelfile
ollama run ecommerce-ner-model
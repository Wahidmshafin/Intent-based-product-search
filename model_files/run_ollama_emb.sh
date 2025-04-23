#!/bin/bash

echo "Starting Ollama server..."
ollama serve &
# Wait for Ollama HTTP API to respond
echo "Waiting for Ollama server to be active..."
sleep 2


if ! ollama list | grep -q 'nomic-embed-text'; then
  echo "Pulling nomic-embed-text..."
  ollama pull nomic-embed-text
fi

# Finally, run the model in the foreground to keep the container alive
echo "Running nomic-embed-text..."
ollama embed nomic-embed-text
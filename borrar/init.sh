#!/bin/bash
which ollama
# Start Ollama in the background.
#/usr/local/bin/ollama serve &
# Record Process ID.
#pid=$!

# Pause for Ollama to start.
#sleep 5

#echo "🔴 Retrieve LLAMA3 model..."
#/usr/local/bin/ollama pull llama3
#echo "🟢 Done!"
# Wait for Ollama process to finish.
#wait $pid
# Start the Python application
echo "Starting Python application..."
python ./run.py

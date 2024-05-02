#!/bin/bash

start_ollama() {
    nohup ollama serve &> /dev/null &
    echo "Ollama service started."
    echo "Process ID: $!"
}

check_ollama_responsive() {
    # Ensure you replace 'your_ollama_port' with the actual port number used by Ollama
    curl --max-time 10 http://localhost:11434/ping
    return $?
}

# Ensure pgrep is available or use alternative
command -v pgrep >/dev/null 2>&1 || { echo >&2 "pgrep is not installed. Installing..."; apt-get install -y procps; }

while true; do
    echo "Checking if Ollama is responsive..."
    if check_ollama_responsive; then
        echo "Ollama is responsive."
    else
        echo "Ollama is not responsive. Attempting to restart..."
        ollama_pid=$(pgrep -f 'ollama')

        if [ ! -z "$ollama_pid" ]; then
            echo "Killing Ollama process: $ollama_pid"
            kill $ollama_pid
            sleep 5  # Ensure process has time to fully exit
        else
            echo "No Ollama process found."
        fi

        start_ollama
    fi

    sleep 10  # Check every 10 minutes
done

import ollama

def restart_ollama():
    try:
        ollama.restart_service()
        print("Ollama service restarted successfully.")
    except Exception as e:
        print(f"Failed to restart Ollama service: {e}")

restart_ollama()
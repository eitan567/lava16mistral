from gradio_client import Client

client = Client("https://cohereforai-c4ai-command-r-plus.hf.space/--replicas/501wi/")
result = client.predict(
							api_name="/lambda"
)
print(result)
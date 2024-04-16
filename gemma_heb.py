# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("yam-peleg/Hebrew-Gemma-11B-V2")
# model = AutoModelForCausalLM.from_pretrained("yam-peleg/Hebrew-Gemma-11B-V2", device_map="auto")

# input_text = "שלום! מה שלומך היום?"
# input_ids = tokenizer(input_text, return_tensors="pt").to("cuda")

# outputs = model.generate(**input_ids)
# print(tokenizer.decode(outputs[0]))


from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

app = Flask(__name__)

# Determine if CUDA (GPU support) is available and set the device accordingly
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("yam-peleg/Hebrew-Gemma-11B-V2")
model = AutoModelForCausalLM.from_pretrained("yam-peleg/Hebrew-Gemma-11B-V2").to(device)

# Define the route for text generation
@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.json
    input_text = data.get("text", "")

    # Tokenize the input text and move tensors to the appropriate device
    input_ids = tokenizer(input_text, return_tensors="pt").to(device)

    # Generate a response using the model
    outputs = model.generate(**input_ids)
    
    # Decode the generated tokens to a string
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({"success": True, "generated_text": generated_text})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

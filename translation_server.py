from flask import Flask, request, jsonify
from transformers import pipeline
import torch  # This import assumes PyTorch is being used

app = Flask(__name__)

# Check if a GPU is available and set the device accordingly
device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU

# Load the translation model and tokenizer on the specified device
translator = pipeline("translation_en_to_he", model="Helsinki-NLP/opus-mt-en-he", device=device)

#using GET
# @app.route('/translate', methods=['GET'])
# def translate_text():
#     data = request
#     english_text = data.values["text"]

#     try:
#         translation = translator(english_text, max_length=512)
#         hebrew_text = translation[0]['translation_text']
#         return jsonify({"success": True, "translation": hebrew_text})
#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

#using POST
@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    english_text = data.get("text", "")

    try:
        translation = translator(english_text, max_length=512)
        hebrew_text = translation[0]['translation_text']
        return jsonify({"success": True, "translation": hebrew_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

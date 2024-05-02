import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

app = Flask(__name__)

modelname = "Salesforce/blip-image-captioning-large"

# Load model and processor
processor = BlipProcessor.from_pretrained(modelname)
model = BlipForConditionalGeneration.from_pretrained(modelname).to("cuda")

@app.route('/caption_controlled', methods=['POST'])
def caption_image_with_instructions():
    data = request.get_json()
    image_path = data.get('path')
    instructions = data.get('instructions', '')  # User-provided instructions or text prompts

    if not image_path:
        return jsonify({"error": "No image path provided"}), 400

    # Try to open the image from the local path
    try:
        with Image.open(image_path) as img:
            raw_image = img.convert('RGB')
    except IOError as e:
        return jsonify({"error": "Unable to open image. Make sure the file path is correct and accessible."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Prepare inputs with instructions if provided
    inputs = processor(raw_image, instructions, return_tensors="pt").to("cuda")

      # Randomize generation parameters
    temperature = np.random.uniform(0.7, 1.3)  # Vary temperature
    top_k = np.random.randint(20, 100)  # Random top_k
    top_p = np.random.uniform(0.7, 0.95)  # Random top_p
    
    # Generate caption based on instructions and creativity parameters
    try:
        out = model.generate(**inputs, max_new_tokens=40)
        caption = processor.decode(out[0], skip_special_tokens=True)

        # Optionally remove the instruction part from the caption
        if caption.lower().startswith(instructions.lower()):
            caption = caption[len(instructions):].lstrip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"caption": caption})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
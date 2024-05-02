from PIL import Image
import requests
from transformers import AutoProcessor, LlavaNextForConditionalGeneration
import torch

# Check if GPU is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf").to(device)
processor = AutoProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")

prompt = "[INST] <image>\nWhat is shown in this image? [/INST]"
url = "https://www.ilankelman.org/stopsigns/australia.jpg"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=prompt, images=image, return_tensors="pt")
inputs = {k: v.to(device) for k, v in inputs.items()}  # Move inputs to the GPU

# Generate
generate_ids = model.generate(**inputs, max_length=30)
result = processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
print(result)

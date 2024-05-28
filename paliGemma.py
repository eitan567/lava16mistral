from PIL import Image
import requests
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration
from huggingface_hub import login

access_token_read = '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'
access_token_write = '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'
login(token = access_token_read)

model = PaliGemmaForConditionalGeneration.from_pretrained("google/PaliGemma-test-224px-hf")
processor = AutoProcessor.from_pretrained("google/PaliGemma-test-224px-hf")

prompt = "answer en Where is the cow standing?"
url = "https://huggingface.co/gv-hf/PaliGemma-test-224px-hf/resolve/main/cow_beach_1.png"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=prompt, images=image, return_tensors="pt")

# Generate
generate_ids = model.generate(**inputs, max_length=30)
processor.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
import piexif
import ollama
import json
import os
import csv
from PIL import Image
from PIL import PngImagePlugin
from PIL.PngImagePlugin import PngInfo
import time
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

def get_title_and_category(filepath):    
    title_prompt = "Generate for me a professional objective and descriptive Title for this image as a 'Title' - Respond using JSON"  
    categories_prompt = "Select the most suitable Category number (between 1 and 21 inclusive), for the main subject in the Image, select the category number only from the following list:"
    categories_prompt += "\n 1. Animals" 
    categories_prompt += "\n 2. Buildings and Architecture" 
    categories_prompt += "\n 3. Business" 
    categories_prompt += "\n 4. Drinks" 
    categories_prompt += "\n 5. The Environment" 
    categories_prompt += "\n 6. States of Mind" 
    categories_prompt += "\n 7. Food" 
    categories_prompt += "\n 8. Graphic Resources" 
    categories_prompt += "\n 9. Hobbies and Leisure" 
    categories_prompt += "\n 10. Industry" 
    categories_prompt += "\n 11. Landscapes" 
    categories_prompt += "\n 12. Lifestyle" 
    categories_prompt += "\n 13. People" 
    categories_prompt += "\n 14. Plants and Flowers" 
    categories_prompt += "\n 15. Culture and Religion" 
    categories_prompt += "\n 16. Science" 
    categories_prompt += "\n 17. Social Issues" 
    categories_prompt += "\n 18. Sports" 
    categories_prompt += "\n 19. Technology" 
    categories_prompt += "\n 20. Transport" 
    categories_prompt += "\n 21. Travel"
    categories_prompt += "\n as a 'Category' - Respond using JSON"

    retries = 3
    while retries > 0:
        try:
            response = ollama.generate(
                model="llava-llama3",#"llava:13b",
                prompt=(title_prompt + ", and " + categories_prompt +
                        "\nexample Response format: " +
                        "{" +
                        "\"Title\": \"Empty Workspace with Laptop\"," +              
                        "\"Category\": 13" +
                        "}"),
                stream=False,
                images=[filepath]
            )

            clean_json = response['response'].strip('`json\n ')
            data = json.loads(clean_json)
            return data['Title'], data['Category']  
        except json.JSONDecodeError:
            print("Failed to decode JSON, retrying...")
            retries -= 1

def get_keywords(filepath):
    keywords_prompt = ("Give me 250 -ONLY one-word- keywords for this image as 'Keywords' - Respond using JSON.\n"
                       "Example Response format: "
                       "{\"Keywords\": ["
                       "\"modern\", \"simple\", \"clean\", \"minimalist\", \"organized\", \"professional\", \"home\", \"tech\", \"workspace\", \"laptop\", \"frame\", \"lamp\", \"plant\", \"white wall\", \"computer\", \"table\", \"pencil\", \"flower\", \"accessories\"]"
                       "]}")

    keywords = set()
    max_loops=4
    retries = 3
    while len(keywords) < 25 and retries > 0 and max_loops > 0:
        try:
            response = ollama.generate(
                model="llava:13b",
                prompt=keywords_prompt,
                stream=False,
                images=[filepath]
            )
            clean_json = response['response'].strip('`json\n ')
            keyword_data = json.loads(clean_json)
            new_keywords = keyword_data['Keywords']

            for keyword in new_keywords:
                if " " not in keyword and keyword not in keywords:
                    keywords.add(keyword)
                    if len(keywords) > 25:
                        print(f"Getting more Keywords. currently {len(keywords)} keywords")
                        break

            if len(keywords) < 25:
                print(f"Getting more Keywords. currently {len(keywords)} keywords")

            max_loops -= 1
        except json.JSONDecodeError:
            print("Failed to decode JSON, retrying...")
            retries -= 1

    return list(keywords)

def sort_keywords_by_importance(keywords, filepath):
    sort_prompt = f"Sort all keywords by importance(return ALL keywords sorted from the most important one at the start to the less at the end): {', '.join(keywords)} - Respond using JSON"
    retries = 3
    while retries > 0:
        try:
            response = ollama.generate(
                model="llava:13b",
                prompt=sort_prompt +
                        "Response format Must be like (JSON Object with 'Keywords' as the key and the array as its value): " +
                        "{" +                
                        "\"Keywords\": [" +
                        "\"modern\", \"simple\", \"clean\", \"minimalist\", \"organized\", \"professional\", \"home\", \"tech\", \"workspace\", \"laptop\", \"frame\", \"lamp\", \"plant\", \"white wall\", \"computer\", \"table\", \"pencil\", \"flower\", \"accessories\"" +
                        "]," +                
                        "}",
                stream=False,
                images=[filepath]  # Provide the image for context
            )

            clean_json = response['response'].strip('`json\n ')
            sorted_keywords = json.loads(clean_json)
            if isinstance(sorted_keywords, list): raise ValueError("sorted keys not json object")
            return (sorted_keywords['Keywords'])[0:49] if len(sorted_keywords['Keywords']) > 49 else sorted_keywords['Keywords']
        except json.JSONDecodeError:
            print("Failed to decode JSON, retrying...")
            retries -= 1
        except Exception:
            print("Failed to decode JSON, retrying...")
            retries -= 1

def load_existing_data(csv_path):
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            existing_data = {row['Filename']: row for row in reader}
        return existing_data
    except FileNotFoundError:
        return {}

def update_jpeg_data(title, keywords, file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No file found at {file_path}")

    with Image.open(file_path) as img:
        if img.format != 'JPEG':
            raise ValueError("Only JPEG files are supported")

        exif_data = img.info.get('exif', b'')
        
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("Title", title)
        metadata.add_text("Keywords", keywords)
        
        img.save(file_path, "JPEG", exif=exif_data, pnginfo=metadata)

        print(f"Metadata updated for {file_path}")

def add_png_metadata(file_path, metadata):
    with Image.open(file_path) as img:
        if img.format != 'PNG':
            raise ValueError("This function is designed to work with PNG files only.")

        pnginfo = PngInfo()
        for key, value in metadata.items():
            if isinstance(value, int):
                value = str(value)            
            pnginfo.add_text(key, value)

        img.save(file_path, "PNG", pnginfo=pnginfo)

def update_jpeg_exif(title, keywords, file_path):
    exif_dict = piexif.load(file_path)
    exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
    exif_dict['0th'][piexif.ImageIFD.XPKeywords] = keywords.encode('utf-16le')
    
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, file_path)

    print(f"EXIF data updated for {file_path}")

def prompt_for_overwrite(filename):
    response = input(f"Entry for {filename} already exists. Overwrite? (y/n): ")
    return response.strip().lower() == 'y'

def get_prefix(filename):
    return filename.rsplit('-', 1)[0]

directory_path = os.environ.get('IMAGE_DIR')
time.sleep(2)

print(f"Directory Path: {directory_path}")

if directory_path is None:
    directory_path = input("Please enter a valid directory path: ")

output_csv_path = os.path.join(directory_path, 'output_data.csv')
existing_data = load_existing_data(output_csv_path)

prefix_data = {}

with open(output_csv_path, 'a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Filename", "Title", "Keywords", "Category"])
    if not existing_data:
        writer.writeheader()
    
    files_array = os.listdir(directory_path)
    for i, filename in enumerate(files_array):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            filepath = os.path.join(directory_path, filename)
            if filename in existing_data:                
                if not prompt_for_overwrite(filename):
                    continue

            prefix = get_prefix(filename)
            if prefix in prefix_data:
                title, keywords, category = prefix_data[prefix]
            else:
                print(f"Processing file {i+1} of {len(files_array)}: {filename}")
                
                title, category = get_title_and_category(filepath)
                keywords = get_keywords(filepath)
                sorted_keywords = sort_keywords_by_importance(keywords, filepath)

                print(f"Title: {title}")
                print(f"Keywords: {', '.join(sorted_keywords)}")
                print(f"Category: {category}")
                print("")

                prefix_data[prefix] = (title, ', '.join(sorted_keywords), category)

            image_data = {
                "Filename": filename,
                "Title": title,
                "Keywords": ', '.join(sorted_keywords),
                "Category": category
            }
            
            if filename in existing_data:
                existing_data.pop(filename)

            writer.writerow(image_data)

            if filename.lower().endswith('.png'):
                add_png_metadata(filepath, image_data)
            elif filename.lower().endswith(('.jpeg', '.jpg')):
                update_jpeg_exif(image_data['Title'], image_data['Keywords'], filepath)

print(f"Data has been written to {output_csv_path}")

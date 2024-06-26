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

load_dotenv()

def get_title_and_category(filepath):
    title_prompt = "Give this image a professional objective description as a 'Title' - Respond using JSON"    
    categories_prompt = "Select the most suitable Category number (between 1 and 21 includsive), for the main subject in the Image, select the category number only from the following list:"
    " 1. Animals" 
    " 2. Buildings and Architecture" 
    " 3. Business" 
    " 4. Drinks" 
    " 5. The Environment" 
    " 6. States of Mind" 
    " 7. Food" 
    " 8. Graphic Resources" 
    " 9. Hobbies and Leisure" 
    " 10. Industry" 
    " 11. Landscapes" 
    " 12. Lifestyle" 
    " 13. People" 
    " 14. Plants and Flowers" 
    " 15. Culture and Religion" 
    " 16. Science" 
    " 17. Social Issues" 
    " 18. Sports" 
    " 19. Technology" 
    " 20. Transport" 
    " 21. Travel"
    " as a 'Category' - Respond using JSON"

    retries = 3
    while retries > 0:
        try:
            response = ollama.generate(
                model="llava:13b",
                prompt=(title_prompt + ", and " + categories_prompt +
                        "example Response format: " +
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
                       "}")

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
            # Debugging log
            
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

            max_loops-=1
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
            # sorted_keywords = response['response'].strip('`json\n ').split(', ')
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

    # Open the image
    with Image.open(file_path) as img:
        # Ensure we're working with a JPEG; this could be adapted for PNGs or other formats
        if img.format != 'JPEG':
            raise ValueError("Only JPEG files are supported")

        # PIL does not fully support editing EXIF data directly, but you can modify what's there or reassign it
        exif_data = img.info.get('exif', b'')
        
        # Create an instance of PngImagePlugin.PngInfo to store metadata
        metadata = PngImagePlugin.PngInfo()
        
        # Add metadata
        metadata.add_text("Title", title)
        metadata.add_text("Keywords", keywords)
        
        # Save the image with updated metadata
        # This involves rewriting the file, so ensure that you handle this operation carefully in production
        img.save(file_path, "JPEG", exif=exif_data, pnginfo=metadata)

        print(f"Metadata updated for {file_path}")


def add_png_metadata(file_path, metadata):
    # Open the existing PNG file
    with Image.open(file_path) as img:
        # Ensure it's a PNG file
        if img.format != 'PNG':
            raise ValueError("This function is designed to work with PNG files only.")

        # Create a PngInfo object to store metadata
        pnginfo = PngInfo()
        # Adding metadata entries
        for key, value in metadata.items():
            if isinstance(value, int):
                value = str(value)            
            pnginfo.add_text(key, value)

        # Save the image with the new metadata
        img.save(file_path, "PNG", pnginfo=pnginfo)

def update_jpeg_exif(title, keywords, file_path):
    # Load the existing EXIF data from a file
    exif_dict = piexif.load(file_path)
    
    # Update EXIF tags (ensure you use the correct tags and formats)
    exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
    # exif_dict['0th'][piexif.ImageIFD.XPTitle] = title.encode('utf-8')
    exif_dict['0th'][piexif.ImageIFD.XPKeywords] = keywords.encode('utf-16le')
    
    
    # Generate EXIF byte data
    exif_bytes = piexif.dump(exif_dict)
    
    # Write back to the same image
    piexif.insert(exif_bytes, file_path)

    print(f"EXIF data updated for {file_path}")

def prompt_for_overwrite(filename):
    response = input(f"Entry for {filename} already exists. Overwrite? (y/n): ")
    return response.strip().lower() == 'y'

directory_path = os.environ.get('IMAGE_DIR')
time.sleep(2)

print(f"Directory Path: {directory_path}")

if directory_path is None:
    directory_path = input("Please enter a valid directory path: ")

output_csv_path = directory_path + '/output_data.csv'
existing_data = load_existing_data(output_csv_path)

with open(output_csv_path, 'a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Filename", "Title", "Keywords", "Category"])
    if not existing_data:
        writer.writeheader()
    
    files_array = os.listdir(directory_path)
    for i, filename in enumerate(files_array):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            filepath = directory_path + "/" + filename
            if filename in existing_data:                
                # if not prompt_for_overwrite(filename):
                    continue  # Skip this file if user chooses not to overwrite

            print(f"Processing file {i+1} of {len(files_array)}: {filename}")
            
            title, category = get_title_and_category(filepath)
            keywords = get_keywords(filepath)
            sorted_keywords = sort_keywords_by_importance(keywords, filepath)

            print(f"Title: {title}")
            print(f"Keywords: {', '.join(sorted_keywords)}")
            print(f"Category: {category}")
            print("")

            image_data = {
                "Filename": filename,
                "Title": title,
                "Keywords": ', '.join(sorted_keywords),
                "Category": category
            }
            
            # Remove existing entry if it's being overwritten
            if filename in existing_data:
                existing_data.pop(filename)

            writer.writerow(image_data)
            root, ext = os.path.splitext(filename)
            if ext == '.png':
                add_png_metadata(filepath,image_data)
            elif ext == '.jpeg' or ext == '.jpg':
                update_jpeg_exif(image_data['Title'], image_data['Keywords'], filepath)

print(f"Data has been written to {output_csv_path}")
            # keywords = get_keywords(filepath)
            # sorted_keywords = sort_keywords_by_importance(keywords, filepath)
            # print(f"Title: {title}")
            # print(f"Keywords: {', '.join(sorted_keywords)}")
            # print(f"Category: {category}")
            # print("")
            # image_data = {
            #     "Filename": filename,
            #     "Title": title,
            #     "Keywords": ', '.join(sorted_keywords),
            #     "Category": category
            # }
            
            # writer.writerow(image_data)
            # if i == 3:  # Process only the first 4 files
            #     break

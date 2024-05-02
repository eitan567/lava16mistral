# import ollama
# import json

# def printData(filepath):
#   res = ollama.generate(
#     model="llava:13b",  
#     prompt = "describe What is in this picture as a 'Title' - Respond using JSON, and give me 50 one-word keywords for it as 'Keywords' -  Respond using JSON. example Response format: "+
#     "{"+
#     "\"Title\": \"Empty Workspace with Laptop\","+
#     "\"Keywords\": ["+
#       "\"modern\", \"simple\", \"clean\", \"minimalist\", \"organized\", \"professional\", \"home office\", \"tech\", \"workspace\", \"laptop\", \"frame\", \"lamp\", \"plant\", \"white wall\", \"desktop computer\", \"table\", \"pencil holder\", \"flower vase\", \"computer accessories\""+
#     "]"+
#     "}",
#     stream = False,
#     images = [filepath] #'c:/mockup.jpg']
#   )

#   clean_json = res['response'].strip('`json\n ')
#   data = json.loads(clean_json)
#   print(data["Title"] + "\n" + ', '.join(data["Keywords"]) + "\n")

# *****************************************************************************************************************************************

# import ollama
# import json
# import os

# def printData(filepath):
    
#     title = "describe What is in this picture as a 'Title' - Respond using JSON"
#     keywords = "give me 50 -ONLY one-word- keywords for it as 'Keywords' -  Respond using JSON"
#     categories = "Select the most suitable Category number, for the main subject in the Image, from the following list:"
#     " 1. Animals" 
#     " 2. Buildings and Architecture" 
#     " 3. Business" 
#     " 4. Drinks" 
#     " 5. The Environment" 
#     " 6. States of Mind" 
#     " 7. Food" 
#     " 8. Graphic Resources" 
#     " 9. Hobbies and Leisure" 
#     " 10. Industry" 
#     " 11. Landscapes" 
#     " 12. Lifestyle" 
#     " 13. People" 
#     " 14. Plants and Flowers" 
#     " 15. Culture and Religion" 
#     " 16. Science" 
#     " 17. Social Issues" 
#     " 18. Sports" 
#     " 19. Technology" 
#     " 20. Transport" 
#     " 21. Travel"
#     " as a 'Category' - Respond using JSON"

#     res = ollama.generate(
#         model="llava:13b",
#         prompt = title + ", and " + keywords + ", and " + categories +
#                 "example Response format: "+
#                 "{"+
#                 "\"Title\": \"Empty Workspace with Laptop\","+
#                 "\"Keywords\": ["+
#                   "\"modern\", \"simple\", \"clean\", \"minimalist\", \"organized\", \"professional\", \"home office\", \"tech\", \"workspace\", \"laptop\", \"frame\", \"lamp\", \"plant\", \"white wall\", \"desktop computer\", \"table\", \"pencil holder\", \"flower vase\", \"computer accessories\""+
#                 "],"+
#                 "\"Category\": 13"+
#                 "}",
#         stream=False,
#         images=[filepath]
#     )

#     # Assuming the response format is JSON inside a string enclosed in markdown code block notation
#     clean_json = res['response'].strip('`json\n ')
#     data = json.loads(clean_json)
#     print(f"Title: {data['Title']}")
#     print(f"Keywords: {', '.join(data['Keywords'])}")
#     print(f"Category: {data['Category']}")
#     print("")

# # Define the directory path from a .env file (assuming you use os.environ to get it)
# directory_path = os.getenv('IMAGE_DIR', 'E:/images for adobe/10 march - 2 april includes/large-illustrations')

# # Loop through every file in the directory
# for filename in os.listdir(directory_path):
#     # Check if the file is an image (add or adjust extensions as needed)
#     if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
#         filepath = os.path.join(directory_path, filename)
#         printData(filepath)


# *****************************************************************************************************************************

import ollama
import json
import os
import csv

def printData(filepath,filename):
    title = "Describe what is in this picture as a 'Title' - Respond using JSON"
    keywords = "Give me 50 -ONLY one-word- keywords for it as 'Keywords' - Respond using JSON"
    categories = "Select the most suitable Category number, for the main subject in the Image, from the following list:"
    
    res = ollama.generate(
        model="llava:13b",
        prompt=(title + ", and " + keywords + ", and " + categories +
                "example Response format: " +
                "{" +
                "\"Title\": \"Empty Workspace with Laptop\"," +
                "\"Keywords\": [" +
                  "\"modern\", \"simple\", \"clean\", \"minimalist\", \"organized\", \"professional\", \"home office\", \"tech\", \"workspace\", \"laptop\", \"frame\", \"lamp\", \"plant\", \"white wall\", \"desktop computer\", \"table\", \"pencil holder\", \"flower vase\", \"computer accessories\"" +
                "]," +
                "\"Category\": 13" +
                "}"),
        stream=False,
        images=[filepath]
    )
    
    clean_json = res['response'].strip('`json\n ')
    data = json.loads(clean_json)
    print(f"File Name: {filename}")
    print(f"Title: {data['Title']}")
    print(f"Keywords: {', '.join(data['Keywords'])}")
    print(f"Category: {data['Category']}")
    print("")
    return {
        "Filename": os.path.basename(filepath),
        "Title": data['Title'],
        "Keywords": ', '.join(data['Keywords']),
        "Category": data['Category']
    }

directory_path = os.getenv('IMAGE_DIR', 'E:/images for adobe/10 march - 2 april includes/large-illustrations')

# Prepare to write to a CSV file
output_csv_path = os.path.join(directory_path, 'output_data.csv')
with open(output_csv_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Filename", "Title", "Keywords", "Category"])
    writer.writeheader()
    i=1
    # Loop through every file in the directory
    files_array = os.listdir(directory_path)
    number_of_files = len(files_array)
    for filename in files_array:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            filepath = os.path.join(directory_path, filename)
            print(f"File {i} out of {number_of_files}")            
            image_data = printData(filepath,filename)
            writer.writerow(image_data)
            if i==4: break
            i+=1

print(f"Data has been written to {output_csv_path}")

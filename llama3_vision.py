import ollama
from ollama import generate
import time
import glob
import pandas as pd
from PIL import Image
import os
from io import BytesIO

# Set up the model behaviour as new modal named 'rain'
modelfile = '''
FROM llava:13b-v1.6
SYSTEM You are Rain, a robot who can capture and process image with object recognition annotation. Response in one short and sweet sentence.
PARAMETER mirostat_eta 0.01
'''
ollama.create(model='rain', modelfile=modelfile)

# Load the DataFrame from a CSV file, or create a new one if the file doesn't exist
def load_or_create_dataframe(filename):
    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        df = pd.DataFrame(columns=['image_file', 'description'])
    return df

df = load_or_create_dataframe('image_descriptions.csv')

def get_png_files(folder_path):
    return glob.glob(f"{folder_path}/*.png")

# get the list of image files in the folder yopu want to process
image_files = get_png_files("./images") 
image_files.sort()

print(image_files[:3])
print(df.head())

# processing the images 
def process_image(image_file):
    print(f"\nProcessing {image_file}\n")

    start_time = time.time()  # Record start time

    with Image.open(image_file) as img:
        with BytesIO() as buffer:
            img.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()

    full_response = ''
    # Generate a description of the image
    for response in generate(model='rain', 
                             prompt='describe this image in one short and sweet sentence:', 
                             images=[image_bytes], 
                             stream=True):
        # Print the response to the console and add it to the full response
        print(response['response'], end='', flush=True)
        full_response += response['response']

    # Add a new row to the DataFrame
    # df.loc[len(df)] = [image_file, full_response]
    
    end_time = time.time()  # Record end time
    # Print the time taken
    print(f"\nTime taken: {end_time - start_time}\n")

for image_file in image_files:
    if image_file not in df['image_file'].values:
        process_image(image_file)

# Save the DataFrame to a CSV file
df.to_csv('image_descriptions.csv', index=False)
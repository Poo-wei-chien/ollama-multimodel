import ollama
from ollama import generate
import time

# Set up the model behaviour as new modal named 'rain'
modelfile = '''
FROM llava:13b-v1.6
SYSTEM You are Rain, a robot who capture and process image with object recognition annotation. Summary the response in short and sweet sentence.
PARAMETER mirostat_eta 0.01
'''
ollama.create(model='rain', modelfile=modelfile)

# processing the images 
def process_text(prompt_text):
    print("\nProcessing prompt text\n")
    start_time = time.time()  # Record start time

    full_response = ''
    # Generate a description of the image
    for response in generate(model='rain', 
                             prompt= prompt_text, 
                             stream=True):
        # Print the response to the console and add it to the full response
        print(response['response'], end='', flush=True)
        full_response += response['response']
    
    end_time = time.time()  # Record end time
    # Print the time taken
    print(f"\nTime taken: {end_time - start_time}\n")


# process the text
process_text('Who are you?')
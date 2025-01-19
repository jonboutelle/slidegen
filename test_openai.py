"""
Simple test script for OpenAI API connection
"""
import json
from openai import OpenAI

print("Script starting...", flush=True)

try:
    print("Loading config...", flush=True)
    with open("config.json", 'r') as f:
        config = json.load(f)
        api_key = config["openai_api_key"]
    print("Config loaded", flush=True)
    
    print("Initializing OpenAI client...", flush=True)
    client = OpenAI(api_key=api_key)
    
    print("Testing API connection with a simple completion...", flush=True)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello"}]
    )
    print(f"Response received: {response.choices[0].message.content}", flush=True)
    
except Exception as e:
    print(f"Error occurred: {str(e)}", flush=True)
    import traceback
    print("Full traceback:", flush=True)
    print(traceback.format_exc(), flush=True)

print("Script finished.", flush=True)

"""
Module for generating images from prompts using DALL-E 3
"""
import json
import os
from openai import OpenAI
import requests
from typing import Optional

class ImageGenerator:
    """Handles image generation using DALL-E 3"""
    
    def __init__(self, config_path: str = "config.json"):
        """Initialize with config file containing API key"""
        with open(config_path, 'r') as f:
            config = json.load(f)
            self.client = OpenAI(api_key=config["openai_api_key"])
        
        # Create images directory if it doesn't exist
        os.makedirs("images", exist_ok=True)

    def generate_image(self, prompt: str) -> str:
        """
        Generate an image from a prompt using DALL-E 3.
        
        Args:
            prompt: Image generation prompt
            
        Returns:
            Path to the generated image file
        """
        print(f"\nGenerating image for prompt: {prompt}")
        
        # Clean filename from prompt
        filename = "".join(x for x in prompt[:30] if x.isalnum() or x in (' ', '-', '_'))
        filename = f"images/dalle3_{filename}.png"
        print(f"Will save to: {filename}")
        
        try:
            print("Calling DALL-E 3 API...")
            try:
                # Generate image using DALL-E 3
                response = self.client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                print("API call successful")
            except Exception as api_error:
                print(f"API Error: {str(api_error)}")
                if hasattr(api_error, 'response'):
                    print(f"API Response: {api_error.response.text if hasattr(api_error.response, 'text') else 'No response text'}")
                raise
            
            # Get image URL from response
            image_url = response.data[0].url
            print(f"Got image URL: {image_url}")
            
            # Download and save the image
            print("Downloading image...")
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(img_response.content)
                print("Image saved successfully")
            else:
                raise Exception(f"Failed to download image from {image_url}: Status {img_response.status_code}")
                
            return filename
            
        except Exception as e:
            print(f"Error details: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text if hasattr(e.response, 'text') else 'No response text'}")
            raise Exception(f"Failed to generate or save image: {str(e)}")

def main():
    """Example usage"""
    import sys
    sys.stdout.flush()  # Force flush any buffered output
    print("Starting image generator...", flush=True)
    
    try:
        print("Initializing ImageGenerator...", flush=True)
        generator = ImageGenerator()
        
        # Example prompt from our LLM output
        prompt = "A military drone flying over a battlefield at sunset, painted in the style of a classical oil painting"
        print(f"Using prompt: {prompt}", flush=True)
        
        try:
            result = generator.generate_image(prompt)
            print(f"\nGenerated image saved to: {result}")
                
        except Exception as e:
            print(f"Error during image generation: {str(e)}")
            import traceback
            print("Full traceback:")
            print(traceback.format_exc())
            
    except Exception as e:
        print(f"Error during initialization: {str(e)}")
        import traceback
        print("Full traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    print("Script starting...", flush=True)
    main()
    print("Script finished.", flush=True)
